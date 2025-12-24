from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from . import views

urlpatterns = [
    path("signup/", views.signup),
    path("login/", views.login),
    path("refresh/", TokenRefreshView.as_view()),

    path("me/", views.me),
    path("profile/", views.update_profile, name="update_profile"),
    path("me/profile/", views.update_profile),
    path("me/theme/", views.update_theme),

    path("users/<str:username>/", views.user_profile),
    path("users/<str:username>/follow/", views.follow_toggle),

    path("social/<str:provider>/", views.social_login_placeholder),
    path('users/<str:username>/follow-list/<str:type>/', views.user_follow_list),
    path("withdraw/", views.withdraw, name="withdraw"),
    path("find-username/", views.find_username, name="find_username"),
    path("password-reset/request/", views.password_reset_request, name="password_reset_request"),
    path("password-reset/confirm/", views.password_reset_confirm, name="password_reset_confirm"),
]
