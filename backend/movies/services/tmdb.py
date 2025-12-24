# backend/movies/services/tmdb.py
import requests
import time
from datetime import datetime
from django.conf import settings
from django.db import transaction

from movies.models import Movie, Genre, MovieGenre, Person, MovieCredit, HomeSectionEntry


TMDB_BASE_URL = "https://api.themoviedb.org/3"


def _tmdb_get(path: str, params=None):
    if params is None:
        params = {}
    params = {
        "api_key": settings.TMDB_API_KEY,
        "language": "ko-KR",
        **params,
    }
    url = f"{TMDB_BASE_URL}{path}"
    r = requests.get(url, params=params, timeout=15)
    r.raise_for_status()
    return r.json()


def _parse_date(s):
    if not s:
        return None
    try:
        return datetime.strptime(s, "%Y-%m-%d").date()
    except Exception:
        return None


@transaction.atomic
def upsert_movie_from_tmdb(movie_json: dict) -> Movie:
    movie, _ = Movie.objects.update_or_create(
        tmdb_id=movie_json["id"],
        defaults={
            "title": movie_json.get("title") or "",
            "original_title": movie_json.get("original_title") or "",
            "overview": movie_json.get("overview") or "",
            "release_date": _parse_date(movie_json.get("release_date")),
            "poster_path": movie_json.get("poster_path") or "",
            "backdrop_path": movie_json.get("backdrop_path") or "",
            "popularity": float(movie_json.get("popularity") or 0),
            "vote_average": float(movie_json.get("vote_average") or 0),
            "vote_count": int(movie_json.get("vote_count") or 0),
        },
    )
    return movie


@transaction.atomic
def upsert_genres(genres_list: list):
    # genres_list: [{"id":..., "name":...}, ...]
    for g in genres_list:
        Genre.objects.update_or_create(
            tmdb_id=g["id"],
            defaults={"name": g.get("name") or ""},
        )


@transaction.atomic
def set_movie_genres(movie: Movie, genre_ids: list[int]):
    # 중복/정합성 단순화를 위해: 기존 매핑 삭제 후 재생성
    MovieGenre.objects.filter(movie=movie).delete()
    genres = Genre.objects.filter(tmdb_id__in=genre_ids)
    for gen in genres:
        MovieGenre.objects.create(movie=movie, genre=gen)


@transaction.atomic
def sync_movie_credits(movie: Movie, cast_limit=10):
    credits = _tmdb_get(f"/movie/{movie.tmdb_id}/credits")

    # 기존 크레딧 제거 후 재생성(정합성 유지)
    MovieCredit.objects.filter(movie=movie).delete()

    # 감독(crew에서 job == Director)
    for crew in credits.get("crew", []):
        if crew.get("job") == "Director":
            person, _ = Person.objects.update_or_create(
                tmdb_id=crew["id"],
                defaults={
                    "name": crew.get("name") or "",
                    "profile_path": crew.get("profile_path") or "",
                    "known_for_department": crew.get("known_for_department") or "",
                },
            )
            MovieCredit.objects.create(
                movie=movie,
                person=person,
                role_type="DIRECTOR",
                job="Director",
                order=0,
            )

    # 출연진(cast 상위 N명)
    for idx, cast in enumerate((credits.get("cast") or [])[:cast_limit]):
        person, _ = Person.objects.update_or_create(
            tmdb_id=cast["id"],
            defaults={
                "name": cast.get("name") or "",
                "profile_path": cast.get("profile_path") or "",
                "known_for_department": cast.get("known_for_department") or "",
            },
        )
        MovieCredit.objects.create(
            movie=movie,
            person=person,
            role_type="CAST",
            character_name=cast.get("character") or "",
            order=int(cast.get("order") or idx),
        )


@transaction.atomic
def sync_home_section(section_code: str, tmdb_path: str, pages=1, with_credits=True):
    # section_code: POPULAR / NOW_PLAYING / TOP_RATED
    HomeSectionEntry.objects.filter(section=section_code).delete()

    rank = 1
    seen_tmdb_ids = set()   # ✅ 중복 방지

    for page in range(1, pages + 1):
        data = _tmdb_get(tmdb_path, params={"page": page})
        results = data.get("results") or []

        for item in results:
            movie = upsert_movie_from_tmdb(item)

            # ✅ 같은 섹션에 같은 영화가 또 나오면 스킵
            if movie.tmdb_id in seen_tmdb_ids:
                continue
            seen_tmdb_ids.add(movie.tmdb_id)

            genre_ids = item.get("genre_ids") or []
            if Genre.objects.exists():
                set_movie_genres(movie, genre_ids)

            # ✅ create 대신 update_or_create (유니크 충돌 안전)
            HomeSectionEntry.objects.update_or_create(
                section=section_code,
                movie=movie,
                defaults={"rank": rank},
            )
            rank += 1

            if with_credits:
                try:
                    sync_movie_credits(movie, cast_limit=10)
                except Exception:
                    pass



def fetch_and_sync_genre_master():
    data = _tmdb_get("/genre/movie/list")
    genres = data.get("genres") or []
    upsert_genres(genres)
    return genres


def fetch_movie_detail_and_update(movie: Movie):
    detail = _tmdb_get(f"/movie/{movie.tmdb_id}")
    # 런타임 등 상세 정보 업데이트
    movie.runtime = detail.get("runtime") or movie.runtime
    movie.overview = detail.get("overview") or movie.overview
    movie.save(update_fields=["runtime", "overview"])

    # 상세의 genres는 [{"id","name"}] 형태라 master도 같이 업데이트 가능
    genres = detail.get("genres") or []
    upsert_genres(genres)
    set_movie_genres(movie, [g["id"] for g in genres])


# backend/movies/services/tmdb.py

import time
from django.db import transaction
from movies.models import Movie, Genre

# ... (기존 코드 유지)

@transaction.atomic
def sync_bulk_movies(pages=25, sort_by="popularity.desc", with_credits=False, with_detail=False, sleep_sec=0.15):
    """
    TMDB discover/movie로 영화 다량 upsert
    - pages=25 -> 500개(20개*25)
    - with_credits: True면 크레딧까지 저장(요청 수 폭증하니 보통 False 추천)
    - with_detail: True면 runtime/genres 보정까지 저장(역시 요청 수 증가)
    """
    total = 0
    for page in range(1, pages + 1):
        data = _tmdb_get(
            "/discover/movie",
            params={
                "sort_by": sort_by,
                "page": page,
                "include_adult": False,
                "include_video": False,
            },
        )
        results = data.get("results") or []

        for item in results:
            movie = upsert_movie_from_tmdb(item)

            # 장르 연결(Genre master가 있어야 함)
            genre_ids = item.get("genre_ids") or []
            if Genre.objects.exists() and genre_ids:
                set_movie_genres(movie, genre_ids)

            if with_detail:
                try:
                    fetch_movie_detail_and_update(movie)
                except Exception:
                    pass

            if with_credits:
                try:
                    sync_movie_credits(movie, cast_limit=10)
                except Exception:
                    pass

            total += 1

        # TMDB 요청 과열 방지(너무 빠르면 막힘/에러 날 수 있음)
        time.sleep(sleep_sec)

    return total
