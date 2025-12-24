from django.urls import path
from . import views

urlpatterns = [
    # 영화 상세 페이지용
    path("movie/<int:tmdb_id>/", views.list_movie_reviews),       # GET: 리뷰 목록
    path("movie/<int:tmdb_id>/create/", views.create_movie_review), # POST: 리뷰 작성
    
    # 리뷰 개별 조작
    path("comments/<int:comment_id>/", views.delete_review_comment), # [추가] 삭제입니댱
    path("<int:review_id>/", views.update_delete_review),         # PUT/DELETE
    path("<int:review_id>/like/", views.toggle_like),             # POST: 좋아요
    
    # 홈 화면용
    path("recent/", views.recent_reviews),                        # GET: 최신 리뷰
    
    # ★ 마이페이지용 (프론트 comet.js의 fetchMyActivity가 여기를 호출함)
    # path("my/", views.my_reviews, name="my_reviews"),
    path("my/", views.my_reviews),   # GET: 내 활동
    
    path("<int:review_id>/comments/", views.list_review_comments),        # 댓글 목록 조회
    path("<int:review_id>/comments/create/", views.create_review_comment), # 댓글 작성
    # [추가] 영화 보고싶어요 토글
    path("movies/<int:tmdb_id>/wish/", views.toggle_movie_wish),
    


    
    path('movie/<int:tmdb_id>/my/', views.get_my_movie_review), # 이 줄 추가 ㅠㅜㅠㅜ 너가 삭제니? 
    
]