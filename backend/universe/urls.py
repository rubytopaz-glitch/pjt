# backend/universe/urls.py
from django.contrib import admin
from django.urls import path, include
from django.conf import settings             # 마이페이지
from django.conf.urls.static import static   # 마이페이지

urlpatterns = [
    path("admin/", admin.site.urls),

    path("api/auth/", include("accounts.urls")),
    path("api/movies/", include("movies.urls")),
    path("api/reviews/", include("reviews.urls")),
    path("api/recommends/", include("recommends.urls")),
    path('api/accounts/', include('accounts.urls')),
]


# 마이페이지    
# [추가] DEBUG 모드일 때 미디어 파일 서빙
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)