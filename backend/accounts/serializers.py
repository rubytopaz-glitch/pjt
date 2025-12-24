from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import UserSetting, Follow

# ✅ 네 프로젝트 경로에 맞게 수정!
from reviews.models import Review      # 예: 리뷰 앱
from movies.models import Movie        # 예: 영화 앱

from django.db.models import Q

User = get_user_model()

class MovieBriefSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movie
        fields = ["tmdb_id", "title", "poster_path", "vote_average"]



class UserSerializer(serializers.ModelSerializer):
    followers_count = serializers.SerializerMethodField()
    following_count = serializers.SerializerMethodField()
    theme = serializers.SerializerMethodField()
    
    is_following = serializers.SerializerMethodField()
    reviewed_movies = serializers.SerializerMethodField()
    
    
    
    class Meta:
        model = User
        fields = [
            "id",
            "username",
            "name",
            "email",
            "birth_date",
            "gender",
            "profile_image",
            "followers_count",
            "following_count",
            "theme",
            "is_following",
            "reviewed_movies",
        ]

    def get_followers_count(self, obj):
        # obj를 팔로우하는 사람 수
        return Follow.objects.filter(to_user=obj).count()

    def get_following_count(self, obj):
        # obj가 팔로우하는 사람 수
        return Follow.objects.filter(from_user=obj).count()

    def get_theme(self, obj):
        if hasattr(obj, "setting") and obj.setting:
            return obj.setting.theme
        return "white"
    
    def get_is_following(self, obj):
        request = self.context.get("request")
        if not request or not request.user.is_authenticated:
            return False
        return Follow.objects.filter(from_user=request.user, to_user=obj).exists()
    
    
    def get_reviewed_movies(self, obj):
        qs = (
            Review.objects
            .filter(user=obj)
            .select_related("movie")
            # ✅ 코멘트 없는 것(=보고싶어요만 체크한 케이스) 제외
            .filter(Q(content__isnull=False) & ~Q(content__exact=""))
            # ✅ (선택) rating이 있는 “진짜 리뷰”만 보여주고 싶으면 이것도 추가
            # .filter(rating__isnull=False)
        )
        seen = set()
        movies = []
        for r in qs:
            m = getattr(r, "movie", None)
            if not m:
                continue
            key = m.tmdb_id  # tmdb_id가 없다면 m.id 등으로 변경
            if key in seen:
                continue
            seen.add(key)
            movies.append(m)

        return MovieBriefSerializer(movies, many=True).data

class SignupSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8)
    password2 = serializers.CharField(write_only=True, min_length=8)

    class Meta:
        model = User
        fields = ["username", "password", "password2", "name", "email", "birth_date", "gender"]

    def validate(self, attrs):
        if attrs["password"] != attrs["password2"]:
            raise serializers.ValidationError("비밀번호가 일치하지 않습니다.")
        if not attrs.get("birth_date"):
            raise serializers.ValidationError("생년월일은 필수입니다.")
        g = attrs.get("gender")
        if g and g not in ["M", "F"]:
            raise serializers.ValidationError("성별 값이 올바르지 않습니다.")
        return attrs

    def create(self, validated_data):
        validated_data.pop("password2")
        password = validated_data.pop("password")

        user = User(**validated_data)
        user.set_password(password)  # ✅ 해시 저장
        user.save()

        UserSetting.objects.get_or_create(user=user)
        return user




from rest_framework import serializers
from django.contrib.auth import get_user_model

User = get_user_model()


class ProfileUpdateSerializer(serializers.ModelSerializer):
    """
    마이페이지 '프로필 수정'용
    - username은 보통 변경 금지(서비스 정책)
    - name/email/birth_date/gender/profile_image 정도만 수정 허용
    """
    class Meta:
        model = User
        # 수정을 허용할 필드만 나열 (username은 제외)
        fields = ["profile_image", "name", "email", "birth_date", "gender", "profile_image"]

    def validate_gender(self, value):
        # gender를 null/blank 허용이면 None/""도 허용
        if value in [None, ""]:
            return value
        if value not in ["M", "F"]:
            raise serializers.ValidationError("성별 값이 올바르지 않습니다.")
        return value


class ThemeSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserSetting
        fields = ["theme"]


class FollowToggleResultSerializer(serializers.Serializer):
    is_following = serializers.BooleanField()
    followers_count = serializers.IntegerField()
    following_count = serializers.IntegerField()


class WithdrawSerializer(serializers.Serializer):
    # 일반 계정이면 password 필요, 소셜/비번없는 계정이면 빈 값 허용
    password = serializers.CharField(required=False, allow_blank=True, write_only=True)


class FindUsernameSerializer(serializers.Serializer):
    email = serializers.EmailField()
    birth_date = serializers.DateField(required=False)  # 선택(있으면 검증에 사용)


class PasswordResetRequestSerializer(serializers.Serializer):
    email = serializers.EmailField()


class PasswordResetConfirmSerializer(serializers.Serializer):
    uid = serializers.CharField()
    token = serializers.CharField()
    new_password = serializers.CharField(min_length=8, write_only=True)
    new_password2 = serializers.CharField(min_length=8, write_only=True)

    def validate(self, attrs):
        if attrs["new_password"] != attrs["new_password2"]:
            raise serializers.ValidationError("비밀번호가 일치하지 않습니다.")
        return attrs
