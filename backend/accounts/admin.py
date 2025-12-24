from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin
from django.contrib.auth import get_user_model

from .models import UserSetting, Follow

User = get_user_model()


@admin.register(User)
class UserAdmin(DjangoUserAdmin):
    # ✅ 지금 User 모델에 실제 존재하는 필드만 표시
    list_display = (
        "id",
        "username",
        "name",
        "email",
        "birth_date",
        "gender",
        "is_staff",
        "is_active",
        "date_joined",
    )
    search_fields = ("username", "email", "name")
    ordering = ("-date_joined",)

    fieldsets = (
        (None, {"fields": ("username", "password")}),
        ("개인정보", {"fields": ("name", "email", "birth_date", "gender", "profile_image")}),
        ("권한", {"fields": ("is_active", "is_staff", "is_superuser", "groups", "user_permissions")}),
        ("중요 날짜", {"fields": ("last_login", "date_joined")}),
    )

    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": ("username", "name", "email", "birth_date", "gender", "password1", "password2"),
        }),
    )


@admin.register(UserSetting)
class UserSettingAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "theme")
    search_fields = ("user__username",)


@admin.register(Follow)
class FollowAdmin(admin.ModelAdmin):
    # ✅ Follow 모델 필드명: from_user, to_user
    list_display = ("id", "from_user", "to_user", "created_at")
    search_fields = ("from_user__username", "to_user__username")
    list_filter = ("created_at",)
