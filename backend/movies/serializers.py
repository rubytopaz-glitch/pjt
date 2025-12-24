from django.db.models import Count
from rest_framework import serializers
from .models import Movie, Genre, Person, MovieCredit


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ["tmdb_id", "name"]


class PersonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Person
        fields = ["tmdb_id", "name", "profile_path", "known_for_department"]


class MovieListSerializer(serializers.ModelSerializer):
    genres = GenreSerializer(many=True, read_only=True)
    top_review = serializers.SerializerMethodField()

    class Meta:
        model = Movie
        fields = [
            "tmdb_id",
            "title",
            "original_title",
            "poster_path",
            "backdrop_path",
            "release_date",
            "vote_average",
            "vote_count",
            "popularity",
            "genres",
            "top_review",
        ]

    def get_top_review(self, obj):
        # ✅ 안전하게: Review 객체에 annotate 붙여서 setter 문제 터지지 않게 values()로 처리
        try:
            from reviews.models import Review  # 필요할 때만 import (순환 방지)
        except Exception:
            return None

        r = (
            Review.objects.filter(movie=obj)
            .annotate(likes_count=Count("likes"))
            .select_related("user")
            .order_by("-likes_count", "-created_at")
            .values("id", "content", "rating", "likes_count", "created_at", "user__username")
            .first()
        )
        if not r:
            return None

        return {
            "id": r["id"],
            "content": r["content"],
            "rating": r["rating"],
            "like_count": r["likes_count"],  # 프론트 호환
            "username": r["user__username"],
            "created_at": r["created_at"],
        }


class MovieDetailSerializer(serializers.ModelSerializer):
    genres = GenreSerializer(many=True, read_only=True)
    directors = serializers.SerializerMethodField()
    cast = serializers.SerializerMethodField()

    class Meta:
        model = Movie
        fields = [
            "tmdb_id",
            "title",
            "original_title",
            "overview",
            "runtime",
            "poster_path",
            "backdrop_path",
            "release_date",
            "vote_average",
            "vote_count",
            "popularity",
            "genres",
            "directors",
            "cast",
        ]

    def _credits_qs(self, movie):
        # 기본 reverse name이 moviecredit_set일 가능성 높아서 모델로 직접 조회
        return MovieCredit.objects.filter(movie=movie).select_related("person")

    def get_directors(self, obj):
        qs = self._credits_qs(obj).filter(role_type="DIRECTOR").order_by("order")
        return [
            {
                "tmdb_id": c.person.tmdb_id,
                "name": c.person.name,
                "profile_path": c.person.profile_path,
                "known_for_department": c.person.known_for_department,
                "job": getattr(c, "job", "") or "",
            }
            for c in qs
        ]

    def get_cast(self, obj):
        qs = self._credits_qs(obj).filter(role_type="CAST").order_by("order")
        return [
            {
                "tmdb_id": c.person.tmdb_id,
                "name": c.person.name,
                "profile_path": c.person.profile_path,
                "known_for_department": c.person.known_for_department,
                "character_name": getattr(c, "character_name", "") or "",
                "order": c.order,
            }
            for c in qs
        ]


class PersonDetailSerializer(serializers.ModelSerializer):
    filmography = serializers.SerializerMethodField()

    class Meta:
        model = Person
        fields = ["tmdb_id", "name", "profile_path", "known_for_department", "filmography"]

    def get_filmography(self, obj):
        # ✅ 이 인물이 참여한 영화들(간단 리스트)
        qs = (
            MovieCredit.objects.filter(person=obj)
            .select_related("movie")
            .order_by("role_type", "order")
        )
        out = []
        seen = set()
        for c in qs:
            m = c.movie
            if not m or m.tmdb_id in seen:
                continue
            seen.add(m.tmdb_id)
            out.append(
                {
                    "tmdb_id": m.tmdb_id,
                    "title": m.title,
                    "poster_path": m.poster_path,
                    "role_type": c.role_type,
                }
            )
        return out
