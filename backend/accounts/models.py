from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError


class User(AbstractUser):
    class Gender(models.TextChoices):
        MALE = "M", "남"
        FEMALE = "F", "여"

    # createsuperuser/기존 가입 흐름에서 터지지 않게 안전장치
    name = models.CharField(max_length=50, blank=True, default="")
    email = models.EmailField(unique=True)

    birth_date = models.DateField(null=True, blank=True)
    gender = models.CharField(max_length=1, choices=Gender.choices, null=True, blank=True)

    
    # 마이페이지 
    # ▼▼▼ [수정] URLField -> ImageField로 변경! ▼▼▼
    # (기존) profile_image = models.URLField(blank=True, default="")
    profile_image = models.ImageField(upload_to='profiles/', blank=True, null=True)

    # 관리자 생성/폼에서 email/name을 요구하도록
    EMAIL_FIELD = "email"
    REQUIRED_FIELDS = ["email", "name"]

    def __str__(self):
        return self.username


class UserSetting(models.Model):
    class Theme(models.TextChoices):
        WHITE = "white", "White"
        NETFLIX = "netflix", "Netflix"
        WAVVE = "wavve", "Wavve"

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="setting")
    theme = models.CharField(max_length=20, choices=Theme.choices, default=Theme.WHITE)

    def __str__(self):
        return f"{self.user.username} setting"


class Follow(models.Model):
    from_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="following_relations")
    to_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="follower_relations")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["from_user", "to_user"], name="unique_follow"),
        ]

    def clean(self):
        if self.from_user_id == self.to_user_id:
            raise ValidationError("자기 자신을 팔로우할 수 없습니다.")

    def save(self, *args, **kwargs):
        self.full_clean()
        return super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.from_user.username} -> {self.to_user.username}"
