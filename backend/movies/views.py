from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status
from rest_framework.pagination import PageNumberPagination
from django.db.models import Prefetch
from .models import Movie, MovieCredit
from django.db.models import Q, Count

from rest_framework.permissions import IsAuthenticated # 마이페이지 

from .models import Movie, Genre, Person, HomeSectionEntry, MovieCredit, PersonLike, GenreLike, MovieLike, LikedPerson # 마이페이지  # 영화상세 
from .serializers import (
    MovieListSerializer,
    MovieDetailSerializer,
    GenreSerializer,
    PersonSerializer,
    PersonDetailSerializer,
)
from .services.tmdb import fetch_movie_detail_and_update, sync_movie_credits


class MoviePagination(PageNumberPagination):
    page_size = 20
    page_size_query_param = "page_size"
    max_page_size = 50


@api_view(["GET"])
@permission_classes([AllowAny])
def home(request):
    popular = (
        Movie.objects.filter(home_entries__section="POPULAR")
        .order_by("home_entries__rank")
        .prefetch_related("genres")[:20]
    )
    now_playing = (
        Movie.objects.filter(home_entries__section="NOW_PLAYING")
        .order_by("home_entries__rank")
        .prefetch_related("genres")[:20]
    )
    top_rated = (
        Movie.objects.filter(home_entries__section="TOP_RATED")
        .order_by("home_entries__rank")
        .prefetch_related("genres")[:20]
    )

    return Response(
        {
            "popular": MovieListSerializer(popular, many=True).data,
            "now_playing": MovieListSerializer(now_playing, many=True).data,
            "top_rated": MovieListSerializer(top_rated, many=True).data,
        }
    )


@api_view(["GET"])
@permission_classes([AllowAny])
def movie_list(request):
    """
    /api/movies/list/?sort=popular|latest|rating&genre=28&page=1
    - genre: Genre.tmdb_id
    """
    qs = Movie.objects.all().prefetch_related("genres")

    genre_tmdb_id = request.query_params.get("genre")
    if genre_tmdb_id:
        qs = qs.filter(genres__tmdb_id=int(genre_tmdb_id))

    sort = request.query_params.get("sort", "popular")
    if sort == "latest":
        qs = qs.order_by("-release_date", "-popularity")
    elif sort == "rating":
        qs = qs.order_by("-vote_average", "-vote_count")
    else:
        qs = qs.order_by("-popularity", "-vote_count")

    paginator = MoviePagination()
    page = paginator.paginate_queryset(qs, request)
    data = MovieListSerializer(page, many=True).data
    return paginator.get_paginated_response(data)


@api_view(["GET"])
@permission_classes([AllowAny])
def movie_detail(request, tmdb_id: int):
    movie = (
        Movie.objects.filter(tmdb_id=tmdb_id)
        .prefetch_related("genres")
        .prefetch_related(
            Prefetch(
                "moviecredit_set",  # ✅ 여기 핵심 (기본 역참조)
                queryset=MovieCredit.objects.select_related("person"),
            )
        )
        .first()
    )
    if not movie:
        return Response(
            {"detail": "영화를 찾을 수 없습니다. TMDB 동기화를 먼저 실행하세요."},
            status=status.HTTP_404_NOT_FOUND,
        )

    # ✅ runtime/genres 등 상세 보정
    try:
        fetch_movie_detail_and_update(movie)
    except Exception:
        pass

    # ✅ 크레딧(감독/배우) DB가 비어있으면 요청 시 자동 동기화
    if not MovieCredit.objects.filter(movie=movie).exists():
        try:
            sync_movie_credits(movie, cast_limit=10)
        except Exception:
            pass

    return Response(MovieDetailSerializer(movie).data)


@api_view(["GET"])
@permission_classes([AllowAny])
def movie_credits(request, tmdb_id: int):
    """
    /api/movies/<tmdb_id>/credits/
    감독/배우만 따로 필요할 때 사용
    """
    movie = Movie.objects.filter(tmdb_id=tmdb_id).first()
    if not movie:
        return Response({"detail": "영화를 찾을 수 없습니다."}, status=404)

    if not MovieCredit.objects.filter(movie=movie).exists():
        try:
            sync_movie_credits(movie, cast_limit=10)
        except Exception:
            pass

    qs = MovieCredit.objects.filter(movie=movie).select_related("person").order_by("order")
    directors = qs.filter(role_type="DIRECTOR")
    cast = qs.filter(role_type="CAST").order_by("order")

    def pack(x):
        return {
            "tmdb_id": x.person.tmdb_id,
            "name": x.person.name,
            "profile_path": x.person.profile_path,
            "known_for_department": x.person.known_for_department,
            "role_type": x.role_type,
            "job": getattr(x, "job", "") or "",
            "character_name": getattr(x, "character_name", "") or "",
            "order": x.order,
        }

    return Response(
        {
            "movie_tmdb_id": movie.tmdb_id,
            "directors": [pack(x) for x in directors],
            "cast": [pack(x) for x in cast],
        }
    )


@api_view(["GET"])
@permission_classes([AllowAny])
def genre_list(request):
    qs = Genre.objects.all().order_by("name")
    return Response(GenreSerializer(qs, many=True).data)


from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from django.shortcuts import get_object_or_404

from .models import Person, MovieCredit
from .serializers import PersonDetailSerializer

@api_view(["GET"])
@permission_classes([AllowAny])
def person_detail(request, tmdb_id: int):
    person = get_object_or_404(Person, tmdb_id=tmdb_id)

    credits = (
        MovieCredit.objects.filter(person=person)
        .select_related("movie")
        .order_by("role_type", "order")
    )

    # ✅ 중복 영화 제거(같은 사람이 같은 영화에 여러 credit 있을 수 있음)
    seen = set()
    directors, cast = [], []

    for c in credits:
        m = c.movie
        if m.tmdb_id in seen:
            continue
        seen.add(m.tmdb_id)

        item = {
            "movie_tmdb_id": m.tmdb_id,
            "movie_title": m.title,
            "poster_path": m.poster_path or "",
            "release_date": m.release_date,
            "vote_average": float(m.vote_average or 0),
            "role_type": c.role_type,
            "character_name": c.character_name or "",
            "job": c.job or "",
        }

        if c.role_type == "DIRECTOR":
            directors.append(item)
        else:
            cast.append(item)

    data = PersonDetailSerializer(person).data
    data["directors"] = directors
    data["cast"] = cast
    return Response(data)



@api_view(["GET"])
@permission_classes([AllowAny])
def search(request):
    """
    /api/movies/search/?q=...&type=movie|person
    """
    q = (request.query_params.get("q") or "").strip()
    search_type = request.query_params.get("type", "movie")

    if not q:
        return Response({"detail": "q가 비었습니다."}, status=status.HTTP_400_BAD_REQUEST)

    if search_type == "person":
        people = Person.objects.filter(name__icontains=q).order_by("name")[:30]
        return Response({"type": "person", "results": PersonSerializer(people, many=True).data})

    movies = (
        Movie.objects.filter(Q(title__icontains=q) | Q(original_title__icontains=q))
        .prefetch_related("genres")
        .order_by("-popularity")[:30]
    )
    return Response({"type": "movie", "results": MovieListSerializer(movies, many=True).data})




# 마이페이지 좋아요 목록 API
@api_view(["GET"])
@permission_classes([IsAuthenticated])
def my_likes_list(request):
    """
    마이페이지: 내가 좋아요한 인물/장르/영화 가져오기
    GET /api/movies/likes/?type=movie  -> 내가 좋아요한 영화
    GET /api/movies/likes/?type=person -> 내가 좋아요한 인물
    """
    
    like_type = request.query_params.get("type", "person")
    user = request.user
    
    if like_type == "person":
        likes = PersonLike.objects.filter(user=request.user).select_related("person")
        people = [l.person for l in likes]
        return Response(PersonSerializer(people, many=True).data)
        
    elif like_type == "genre":
        likes = GenreLike.objects.filter(user=request.user).select_related("genre")
        genres = [l.genre for l in likes]
        return Response(GenreSerializer(genres, many=True).data)
    
    elif like_type == "movie": # [추가됨] 영화 좋아요 목록
        likes = MovieLike.objects.filter(user=request.user).select_related("movie")
        movies = [l.movie for l in likes]
        return Response(MovieListSerializer(movies, many=True).data)
    
        
    return Response([])


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def my_movie_likes(request):
    """
    내가 좋아요한 장르나 인물 목록을 가져옵니다.
    ?type=genre|person
    """
    like_type = request.query_params.get("type")
    
    # 아직 좋아요 모델이 구체화되지 않았다면 일단 빈 배열을 반환하여 404를 해결합니다.
    # 나중에 관련 모델(GenreLike 등)을 만드시면 필터링 로직을 넣으세요.
    return Response([])



@api_view(["GET"])
@permission_classes([AllowAny])
def movie_similar(request, tmdb_id: int):
    """
    [비슷한 작품 추천 로직]
    1. 해당 영화의 장르들을 가져옵니다.
    2. 그 장르를 포함하는 다른 영화들을 찾습니다.
    3. 겹치는 장르가 많은 순서 + 인기도 순으로 정렬하여 20개를 뽑습니다.
    """
    movie = get_object_or_404(Movie, tmdb_id=tmdb_id)
    movie_genres = movie.genres.all()

    if not movie_genres.exists():
        # 장르 정보가 없으면 그냥 인기 영화 반환
        similar_movies = Movie.objects.exclude(id=movie.id).order_by("-popularity")[:20]
    else:
        # 같은 장르를 가진 영화들 찾기 (현재 영화 제외)
        similar_movies = (
            Movie.objects.filter(genres__in=movie_genres)
            .exclude(id=movie.id)
            .annotate(same_genres=Count("genres")) # 겹치는 장르 개수 세기
            .order_by("-same_genres", "-popularity") # 많이 겹치고 + 인기 많은 순
            .distinct()[:20]
        )

    return Response(MovieListSerializer(similar_movies, many=True).data)


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def movie_like_toggle(request, tmdb_id: int):
    """
    영화 좋아요 토글 (눌렀다 뗐다)
    """
    movie = get_object_or_404(Movie, tmdb_id=tmdb_id)
    user = request.user

    # 이미 좋아요 했으면 취소
    like_obj = MovieLike.objects.filter(user=user, movie=movie).first()
    
    if like_obj:
        like_obj.delete()
        liked = False
    else:
        MovieLike.objects.create(user=user, movie=movie)
        liked = True
    
    return Response({"liked": liked, "tmdb_id": tmdb_id})


















# 1. 인물 좋아요 토글 (추가/삭제)
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def toggle_person_like(request, person_id):
    user = request.user
    
    # 중복 체크: 이미 좋아요 한 인물인지 확인
    # (주의: LikedPerson 모델을 사용합니다)
    liked_obj = LikedPerson.objects.filter(user=user, person_id=person_id).first()

    if liked_obj:
        # 이미 있으면 삭제 (좋아요 취소)
        liked_obj.delete()
        return Response({'liked': False})
    else:
        # 없으면 새로 생성 (좋아요)
        # 프론트엔드에서 보내준 이름, 사진 경로 등을 함께 저장
        LikedPerson.objects.create(
            user=user,
            person_id=person_id,
            name=request.data.get('name', 'Unknown'),
            profile_path=request.data.get('profile_path', ''),
            department=request.data.get('known_for_department', '')
        )
        return Response({'liked': True})

# 2. 내 좋아요 목록 조회 (마이페이지용)
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_my_liked_people(request):
    likes = LikedPerson.objects.filter(user=request.user).order_by('-created_at')
    
    # 프론트엔드가 사용하기 편한 구조로 변환
    data = [{
        'tmdb_id': p.person_id,  
        'name': p.name,
        'profile_path': p.profile_path,
        'known_for_department': p.department
    } for p in likes]
    
    return Response(data)