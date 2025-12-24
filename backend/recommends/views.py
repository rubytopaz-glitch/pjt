from django.contrib.auth import get_user_model
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Q, Count, Avg, Prefetch
from movies.models import Movie, Genre, Person
from movies.serializers import MovieListSerializer, PersonSerializer

from reviews.models import Review
try:
    from reviews.models import ReviewLike
except Exception:
    ReviewLike = None

try:
    from accounts.models import Follow
except Exception:
    Follow = None

from .services.ai import GENRE_LIST, run_taste_ai
from .models import TastePromptLog

import re
from django.db.models import Q, Count

EXCLUDE_PATTERN = r"([가-힣A-Za-z0-9\s·:_\-]+?)\s*(?:은|는|을|를)?\s*(?:빼고|제외|말고|빼줘|제외해|제외해줘)"

def parse_excludes_from_message(message: str):
    """
    예)
    - '체인소맨 빼고' -> exclude_titles=['체인소맨']
    - '애니메이션은 제외해줘' -> exclude_genres=['애니메이션']
    - '체인소맨, 드라큘라 제외' -> exclude_titles=['체인소맨','드라큘라']
    """
    if not message:
        return [], []

    hits = re.findall(EXCLUDE_PATTERN, message)
    exclude_genres, exclude_titles = [], []

    for h in hits:
        term = (h or "").strip()
        term = term.replace("영화", "").strip()
        if not term:
            continue

        parts = re.split(r"[,\n]|그리고|랑|하고|&|/", term)
        parts = [p.strip() for p in parts if p.strip()]

        for p in parts:
            if p in GENRE_LIST:
                exclude_genres.append(p)
            else:
                exclude_titles.append(p)

    # 중복 제거
    exclude_genres = list(dict.fromkeys(exclude_genres))
    exclude_titles = list(dict.fromkeys(exclude_titles))
    return exclude_genres, exclude_titles


def build_title_q(field: str, terms: list[str]) -> Q:
    q = Q()
    for t in terms:
        q |= Q(**{f"{field}__icontains": t})
    return q


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def ai_taste(request):
    """
    POST /api/recommends/ai/
    body: { "message": "...", "history": [...] }
    """
    message = (request.data.get("message") or "").strip()
    history = request.data.get("history") or []

    if not message:
        return Response({"detail": "message가 비었습니다."}, status=status.HTTP_400_BAD_REQUEST)

    # 1) AI 분석
    data, raw = run_taste_ai(message, history=history)

    # 로그 저장
    try:
        TastePromptLog.objects.create(
            user=request.user,
            prompt=message,
            response_raw=raw,
            response_json=data if isinstance(data, dict) else None,
        )
    except Exception:
        pass

    # 2) 필터 추출 (AI + 메시지 파싱)
    filters = data.get("filters") or {}

    primary = filters.get("primary_genre_name")  # 있으면 활용 (없어도 OK)
    genre_names = filters.get("genre_names") or []
    keywords = filters.get("keywords") or []
    titles = filters.get("titles") or []
    min_vote = float(filters.get("min_vote") or 0)
    strict = bool(filters.get("strict")) if isinstance(filters.get("strict"), (bool, int)) else False

    # ✅ 새로 추가될 필드(유저 ai 코드에서 추가 예정)
    exclude_genres_ai = filters.get("exclude_genre_names") or []
    exclude_titles_ai = filters.get("exclude_titles") or []  # 없으면 []

    # ✅ 사용자가 직접 쓴 "빼고/제외"는 AI가 실수해도 강제 제외
    exclude_genres_msg, exclude_titles_msg = parse_excludes_from_message(message)

    exclude_genre_names = list(dict.fromkeys([*exclude_genres_ai, *exclude_genres_msg]))
    exclude_titles = list(dict.fromkeys([*exclude_titles_ai, *exclude_titles_msg]))

    # ✅ (중요) exclude_titles에 있는 건 titles(포함 후보)에서 제거 (체인소맨 포함 방지)
    titles = [t for t in titles if t not in exclude_titles]

    # include 장르 구성: primary를 맨 앞에 두고 중복 제거
    include_genres = []
    if isinstance(primary, str) and primary.strip():
        include_genres.append(primary.strip())
    include_genres += [g for g in genre_names if isinstance(g, str) and g.strip()]
    # 중복 제거 + exclude 제거
    include_genres = list(dict.fromkeys([g for g in include_genres if g not in exclude_genre_names]))

    # 3) DB 쿼리 시작
    base_qs = Movie.objects.all().prefetch_related("genres")

    # ✅ A) 제외 장르 먼저 적용 (가장 먼저!)
    if exclude_genre_names:
        base_qs = base_qs.exclude(genres__name__in=exclude_genre_names)

    # ✅ B) 제외 제목 적용 (체인소맨 빼고)
    if exclude_titles:
        base_qs = base_qs.exclude(build_title_q("title", exclude_titles))

    # ✅ C) 평점 컷
    if min_vote > 0:
        base_qs = base_qs.filter(vote_average__gte=min_vote)

    # 키워드 Q (OR로 묶되, 전체 흐름에서는 AND처럼 적용)
    k_q = Q()
    if keywords:
        for k in keywords:
            k = (k or "").strip()
            if not k:
                continue
            k_q |= Q(title__icontains=k) | Q(overview__icontains=k)

    # -----------------------------
    # ✅ 4) "좋은 결과" 우선 전략: 장르/키워드를 기본으로, 없으면 점진적 완화
    # -----------------------------
    qs = base_qs

    # (1) 장르 적용
    if include_genres:
        if strict:
            # strict: 장르 모두 만족(AND)
            for g in include_genres:
                qs = qs.filter(genres__name=g)
            qs = qs.distinct()
        else:
            # non-strict: 장르 일치 개수로 랭킹 (많이 맞을수록 위)
            qs = qs.annotate(
                match_genres=Count("genres", filter=Q(genres__name__in=include_genres), distinct=True)
            ).distinct()

    # (2) 키워드 적용 (가능하면 유지)
    qs_with_kw = qs
    if k_q:
        qs_with_kw = qs.filter(k_q).distinct()

    # ✅ 결과가 너무 적으면 fallback: 키워드 제거하고 장르만
    if k_q and not qs_with_kw.exists():
        qs_final = qs
    else:
        qs_final = qs_with_kw

    # ✅ 그래도 없으면 fallback: 장르도 제거하고 키워드만(단, exclude는 유지됨)
    if include_genres and not qs_final.exists() and k_q:
        qs_final = base_qs.filter(k_q).distinct()

    # ✅ 그래도 없으면 마지막 fallback: titles 매칭(단, exclude_titles는 이미 빠짐)
    if not qs_final.exists() and titles:
        t_q = Q()
        for t in titles:
            t_q |= Q(title__icontains=t)
        qs_final = base_qs.filter(t_q).distinct()

    # -----------------------------
    # ✅ 5) 정렬 (non-strict면 match_genres 우선)
    # -----------------------------
    if not strict and include_genres:
        qs_final = qs_final.order_by("-match_genres", "-popularity", "-vote_average")
    else:
        qs_final = qs_final.order_by("-popularity", "-vote_average")

    qs_final = qs_final[:12]

    serialized = MovieListSerializer(qs_final, many=True).data

    # (선택) AI가 준 recommended_reasons가 있으면 title 기준으로 매핑해서 tmdb_id 키로 내려주기
    reasons_by_title = data.get("recommended_reasons") or {}
    reasons_by_tmdb = {}
    if isinstance(reasons_by_title, dict):
        for m in serialized:
            tmdb_id = m.get("tmdb_id")
            title = m.get("title")
            if tmdb_id and title and title in reasons_by_title:
                reasons_by_tmdb[str(tmdb_id)] = reasons_by_title[title]

    return Response({
        "answer": data.get("answer", "조건에 맞는 영화를 찾아보았습니다."),
        "filters": {
            **filters,
            "exclude_genre_names": exclude_genre_names,
            "exclude_titles": exclude_titles,
        },
        "movies": serialized,
        "recommended_reasons": reasons_by_tmdb,  # 프론트에서 카드에 붙여쓰기 쉬움
    })



@api_view(["GET"])
@permission_classes([AllowAny])
def genre_recommend(request):
    genre_tmdb_id = request.query_params.get("genre")
    if not genre_tmdb_id:
        genres = Genre.objects.all().order_by("name")
        return Response({"genres": [{"tmdb_id": g.tmdb_id, "name": g.name} for g in genres]})
    qs = Movie.objects.filter(genres__tmdb_id=int(genre_tmdb_id)).prefetch_related("genres").order_by("-popularity")[:24]
    return Response({"results": MovieListSerializer(qs, many=True).data})

@api_view(["GET"])
@permission_classes([AllowAny])
def people_recommend(request):
    q = (request.query_params.get("q") or "").strip()
    if q:
        people = Person.objects.annotate(credits_count=Count("movies")).filter(name__icontains=q, credits_count__gt=0).order_by("-credits_count")[:30]
        return Response({"results": PersonSerializer(people, many=True).data})
    try:
        people = Person.objects.annotate(credits_count=Count("movies")).filter(credits_count__gt=0).order_by("-credits_count", "name")[:40]
    except Exception:
        people = Person.objects.filter(movies__isnull=False).distinct()[:20]
    return Response({"results": PersonSerializer(people, many=True).data})

@api_view(["GET"])
@permission_classes([IsAuthenticated])
def user_recommend(request):
    User = get_user_model()
    me = request.user
    top_reviewers_raw = Review.objects.values("user_id").annotate(cnt=Count("id")).order_by("-cnt")[:10]
    reviewer_ids = [r["user_id"] for r in top_reviewers_raw]
    reviewer_cnt_map = {r["user_id"]: r["cnt"] for r in top_reviewers_raw}
    reviewers = list(User.objects.filter(id__in=reviewer_ids))
    top_liked_users = []
    if ReviewLike is not None:
        top_liked_raw = ReviewLike.objects.values("review__user_id").annotate(cnt=Count("id")).order_by("-cnt")[:10]
        liked_ids = [r["review__user_id"] for r in top_liked_raw]
        liked_cnt_map = {r["review__user_id"]: r["cnt"] for r in top_liked_raw}
        liked_users = list(User.objects.filter(id__in=liked_ids))
        top_liked_users = [{"id": u.id, "username": getattr(u, "username", ""), "received_likes": liked_cnt_map.get(u.id, 0)} for u in liked_users]
    suggested = []
    if Follow is not None:
        try:
            following_ids = set(Follow.objects.filter(follower=me).values_list("following_id", flat=True))
            base = User.objects.exclude(id=me.id).exclude(id__in=following_ids).annotate(reviews_count=Count("reviews")).order_by("-reviews_count")[:10]
            suggested = [{"id": u.id, "username": getattr(u, "username", ""), "reviews_count": getattr(u, "reviews_count", 0)} for u in base]
        except Exception: pass
    return Response({"top_reviewers": [{"id": u.id, "username": getattr(u, "username", ""), "reviews_count": reviewer_cnt_map.get(u.id, 0)} for u in reviewers], "top_liked": top_liked_users, "suggested": suggested})

GENRE_LABELS = ["드라마","SF","판타지","로맨스","뮤지컬","애니메이션","전쟁","가족","다큐멘터리","스릴러","공포","액션"]

@api_view(["GET"])
@permission_classes([IsAuthenticated])
def taste_summary(request):
    me = request.user
    my_reviews_qs = Review.objects.filter(user=me).select_related("movie").order_by("-created_at")
    tmdb_ids = list(my_reviews_qs.values_list("movie__tmdb_id", flat=True).distinct())
    watched_movies_qs = Movie.objects.filter(tmdb_id__in=tmdb_ids)
    watched_count = len(tmdb_ids)
    watched_data = []
    for review in my_reviews_qs:
        watched_data.append({
            "tmdb_id": review.movie.tmdb_id,
            "title": review.movie.title,
            "poster_path": review.movie.poster_path,
            "genres": [g.name for g in review.movie.genres.all()], # 장르 필터링용
            "my_rating": review.rating # ⭐ 내 평점 데이터 추가
        })

    watched_count = len(watched_data)
    
    if watched_count == 0:
        return Response({"watched_count": 0, "top_genre": "-", "avg_rating": 0, "recent_movie_title": "", "genre_scores": {}, "watched_movies": [],"recommended_movies": [], "detail": "작성된 리뷰가 없습니다."})
    avg_rating = round(float(my_reviews_qs.aggregate(avg=Avg("rating"))["avg"] or 0), 1)
    latest_review = my_reviews_qs.first()
    recent_movie_title = latest_review.movie.title if latest_review else ""
    genre_rows = Movie.objects.filter(tmdb_id__in=tmdb_ids).values("genres__name").annotate(cnt=Count("genres__name")).order_by("-cnt")
    genre_count_map = {row["genres__name"]: row["cnt"] for row in genre_rows if row["genres__name"]}
    top_genres_sorted = sorted(genre_count_map.items(), key=lambda x: x[1], reverse=True)
    top_genre = "/".join([g for g, _ in top_genres_sorted[:2]]) if top_genres_sorted else "-"
    max_cnt = max(genre_count_map.values(), default=0)
    genre_scores = {label: int((genre_count_map.get(label, 0) / max_cnt) * 100) if max_cnt else 0 for label in GENRE_LABELS}
    top_genre_names = [g for g, _ in top_genres_sorted[:2]]
    rec_qs = Movie.objects.all().prefetch_related("genres")
    if top_genre_names: rec_qs = rec_qs.filter(genres__name__in=top_genre_names).distinct()
    if tmdb_ids: rec_qs = rec_qs.exclude(tmdb_id__in=tmdb_ids)
    rec_qs = rec_qs.order_by("-popularity")[:12]
    return Response({"watched_count": watched_count, "top_genre": top_genre, "avg_rating": avg_rating, "recent_movie_title": recent_movie_title, "genre_scores": genre_scores, "watched_movies": watched_data, "recommended_movies": MovieListSerializer(rec_qs, many=True).data})