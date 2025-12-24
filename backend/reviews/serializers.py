# backend/reviews/serializers.py
from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Review
from movies.serializers import MovieListSerializer

User = get_user_model()

# ✅ 유저 정보를 객체로 보내기 위한 시리얼라이저 (익명 방지)
class ReviewUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "profile_image"]

class ReviewCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ["content", "watched", "rating"]

    def validate(self, attrs):
        watched = attrs.get("watched", None)
        rating = attrs.get("rating", None)
        content = (attrs.get("content") or "").strip()

        if watched is not True:
            raise serializers.ValidationError("리뷰 작성은 '봤어요' 체크가 필요합니다.")
        if rating is None:
            raise serializers.ValidationError("별점은 필수입니다.")
        if not (1 <= rating <= 5):
            raise serializers.ValidationError("별점은 1~5 사이여야 합니다.")
        if not content:
            raise serializers.ValidationError("한줄평을 입력해 주세요.")
        return attrs

class ReviewSerializer(serializers.ModelSerializer):
    # ✅ 중요: user를 숫자가 아닌 객체(정보)로 내보냄
    user = ReviewUserSerializer(read_only=True)
    movie = MovieListSerializer(read_only=True)
    user_username = serializers.ReadOnlyField(source='user.username')

    # ✅ DB annotate 수치와 프론트 사용 필드명(like_count) 통일
    likes_count = serializers.IntegerField(read_only=True)
    like_count = serializers.SerializerMethodField()
    is_liked = serializers.SerializerMethodField()
    
    comments_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = Review
        fields = [
            "id",
            "movie",
            "user",
            "user_username",
            "content",
            "watched",
            "rating",
            "likes_count",
            "like_count",
            "is_liked",
            "created_at",
            "updated_at",
            "comments_count",
        ]
        read_only_fields = ["id", "movie", "user", "likes_count", "created_at", "updated_at"]

    def get_like_count(self, obj):
        # annotate된 값이 있으면 쓰고, 없으면 DB 직접 조회
        if hasattr(obj, "likes_count") and obj.likes_count is not None:
            return obj.likes_count
        return obj.likes.count()

    def get_is_liked(self, obj):
        request = self.context.get("request")
        if not request or not request.user.is_authenticated:
            return False
        return obj.likes.filter(id=request.user.id).exists()

class RecentReviewSerializer(serializers.ModelSerializer):
    user = ReviewUserSerializer(read_only=True)
    # 홈 화면 카드용 영화 정보
    movie = MovieListSerializer(read_only=True)
    
    likes_count = serializers.IntegerField(read_only=True)
    like_count = serializers.SerializerMethodField()
    is_liked = serializers.SerializerMethodField()
    # ✅ [필수] 이 줄이 없으면 프론트에서 댓글 개수를 못 읽어서 카드가 안 뜰 수 있음!
    comments_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = Review
        fields = [
            "id",
            "user",
            "movie",
            "content",
            "rating",
            "likes_count",
            "like_count",
            "is_liked",
            "created_at",
            "comments_count",
        ]

    def get_like_count(self, obj):
        if hasattr(obj, "likes_count") and obj.likes_count is not None:
            return obj.likes_count
        return obj.likes.count()

    def get_is_liked(self, obj):
        request = self.context.get("request")
        if not request or not request.user.is_authenticated:
            return False
        return obj.likes.filter(id=request.user.id).exists()
    