from django.urls import path
from . import views

urlpatterns = [
    path("home/", views.home),
    path("list/", views.movie_list),
    path("genres/", views.genre_list),
    path("search/", views.search),

    # ✅ movie detail & similar & like
    path("<int:tmdb_id>/", views.movie_detail),
    path("<int:tmdb_id>/credits/", views.movie_credits),
    path("<int:tmdb_id>/similar/", views.movie_similar),      # [추가] 비슷한 영화
    path("<int:tmdb_id>/like/", views.movie_like_toggle),     # [추가] 좋아요 토글

    # ✅ people
    path("people/<int:tmdb_id>/", views.person_detail),
    # path("likes/", views.my_movie_likes, name="my_movie_likes"),
    path("likes/", views.my_likes_list),                      # [수정] 통합된 좋아요 리스트 함수 연결
    
    
    
    
    # [추가] 인물 좋아요 토글 URL
    path('people/<int:person_id>/like/', views.toggle_person_like),

    # [추가] 마이페이지 내 좋아요 목록 URL
    path('me/liked-people/', views.get_my_liked_people),
    
    
]
