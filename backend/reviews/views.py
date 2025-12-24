from django.db.models import Count
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from django.shortcuts import get_object_or_404

from movies.models import Movie 
from .models import Review, ReviewComment 
from .serializers import ReviewSerializer, ReviewCreateSerializer, RecentReviewSerializer

# 1. 리뷰 목록 조회
@api_view(["GET"])
@permission_classes([AllowAny])
def list_movie_reviews(request, tmdb_id: int):
    movie = get_object_or_404(Movie, tmdb_id=tmdb_id)
    qs = (
        Review.objects.filter(movie=movie, watched=True) # ✅ 빈 코멘트 제외
        .select_related("user", "movie")
        .annotate(likes_count=Count("likes", distinct=True), comments_count=Count("comments", distinct=True))
        .order_by("-likes_count", "-created_at")
    )
    return Response(ReviewSerializer(qs, many=True, context={"request": request}).data)

# 2. 리뷰 작성
@api_view(["POST"])
@permission_classes([IsAuthenticated])
def create_movie_review(request, tmdb_id: int):
    movie = get_object_or_404(Movie, tmdb_id=tmdb_id)
    if Review.objects.filter(movie=movie, user=request.user).exists():
        return Response({"detail": "이미 리뷰가 존재합니다."}, status=409)

    serializer = ReviewCreateSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)

    review = Review.objects.create(
        movie=movie, user=request.user,
        content=serializer.validated_data["content"],
        watched=serializer.validated_data.get("watched", False),
        rating=serializer.validated_data["rating"],
    )
    # 리턴 시 user 정보 포함
    out = Review.objects.filter(id=review.id).select_related("user", "movie").annotate(likes_count=Count("likes"), comments_count=Count("comments")).first()
    return Response(ReviewSerializer(out, context={"request": request}).data, status=201)

# 3. 리뷰 수정/삭제
@api_view(["PUT", "DELETE"])
@permission_classes([IsAuthenticated])
def update_delete_review(request, review_id: int):
    review = get_object_or_404(Review, id=review_id)
    if review.user_id != request.user.id:
        return Response({"detail": "권한이 없습니다."}, status=403)

    if request.method == "DELETE":
        review.delete()
        return Response(status=204)

    serializer = ReviewCreateSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    review.content = serializer.validated_data["content"]
    review.watched = serializer.validated_data.get("watched", review.watched)
    review.rating = serializer.validated_data["rating"]
    review.save()
    
    out = Review.objects.filter(id=review.id).select_related("user", "movie").annotate(likes_count=Count("likes"), comments_count=Count("comments")).first()
    return Response(ReviewSerializer(out, context={"request": request}).data)

# 4. 좋아요 토글
@api_view(["POST"])
@permission_classes([IsAuthenticated])
def toggle_like(request, review_id: int):
    review = get_object_or_404(Review, id=review_id)
    if review.user_id == request.user.id:
        return Response({"detail": "본인 글에는 좋아요 불가"}, status=400)
    
    if review.likes.filter(id=request.user.id).exists():
        review.likes.remove(request.user)
        liked = False
    else:
        review.likes.add(request.user)
        liked = True
    return Response({"liked": liked, "like_count": review.likes.count()})

# 5. 최근 리뷰 (홈 화면)
@api_view(["GET"])
@permission_classes([AllowAny])
def recent_reviews(request):
    limit = int(request.query_params.get("limit", 12))
    qs = (
        Review.objects.filter(watched=True) # ✅ 빈 코멘트 제외
        .select_related("user", "movie")
        .annotate(likes_count=Count("likes", distinct=True), comments_count=Count("comments", distinct=True))
        .order_by("-created_at")[:limit]
    )
    return Response(RecentReviewSerializer(qs, many=True, context={"request": request}).data)

# 6. [핵심] 마이페이지 통합 뷰
@api_view(["GET"])
@permission_classes([IsAuthenticated])
def my_reviews(request):
    status_param = request.query_params.get("status", "commented")
    sort_param = request.query_params.get("sort", "latest")
    user = request.user

    if status_param == "liked":
        qs = user.liked_reviews.select_related("movie", "user").filter(watched=True)
    else:
        qs = Review.objects.filter(user=user).select_related("movie", "user")
        if status_param == "wish":
            qs = qs.filter(watched=False) # ✅ 보고싶어요만
        else:
            qs = qs.filter(watched=True)  # ✅ 코멘트만 (빈 것 제외)

    qs = qs.annotate(likes_count=Count("likes", distinct=True), comments_count=Count("comments", distinct=True))
    
    if sort_param == "latest": qs = qs.order_by("-created_at")
    elif sort_param == "rating_high": qs = qs.order_by("-rating", "-created_at")
    
    return Response(ReviewSerializer(qs, many=True, context={"request": request}).data)

# 7. 보고싶어요 토글
@api_view(["POST"])
@permission_classes([IsAuthenticated])
def toggle_movie_wish(request, tmdb_id: int):
    movie = get_object_or_404(Movie, tmdb_id=tmdb_id)
    review = Review.objects.filter(movie=movie, user=request.user).first()

    if review:
        if review.watched:
            return Response({"detail": "이미 감상한 작품입니다."}, status=400)
        review.delete()
        return Response({"wished": False, "message": "취소됨"})
    else:
        Review.objects.create(movie=movie, user=request.user, watched=False, rating=0, content="")
        return Response({"wished": True, "message": "등록됨"})

# 8. 대댓글 작성 (ID 포함)
@api_view(["POST"])
@permission_classes([IsAuthenticated])
def create_review_comment(request, review_id):
    review = get_object_or_404(Review, id=review_id)
    content = request.data.get("content")
    if not content: return Response(status=400)
    
    comment = ReviewComment.objects.create(review=review, user=request.user, content=content)
    return Response({
        "id": comment.id,
        "content": comment.content,
        "user": { "id": comment.user.id, "username": comment.user.username, "profile_image": comment.user.profile_image.url if comment.user.profile_image else None },
        "created_at": comment.created_at
    })

# 9. 대댓글 목록 (ID 포함)
@api_view(["GET"])
@permission_classes([AllowAny])
def list_review_comments(request, review_id):
    comments = ReviewComment.objects.filter(review_id=review_id).select_related('user').order_by('created_at')
    data = []
    for c in comments:
        data.append({
            "id": c.id,
            "content": c.content,
            "user": { "id": c.user.id, "username": c.user.username, "profile_image": c.user.profile_image.url if c.user.profile_image else None },
            "created_at": c.created_at
        })
    return Response(data)

# 10. 대댓글 삭제
@api_view(["DELETE"])
@permission_classes([IsAuthenticated])
def delete_review_comment(request, comment_id):
    comment = get_object_or_404(ReviewComment, id=comment_id)
    if comment.user != request.user: return Response(status=403)
    comment.delete()
    return Response(status=204)










# [추가] 특정 영화에 대한 내 리뷰 조회 (작성 여부 확인용)
@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_my_movie_review(request, tmdb_id: int):
    movie = get_object_or_404(Movie, tmdb_id=tmdb_id)

    review = (
        Review.objects
        .filter(movie=movie, user=request.user)
        .select_related("user", "movie")
        .annotate(
            likes_count=Count("likes", distinct=True),
            comments_count=Count("comments", distinct=True),
        )
        .first()
    )

    if not review:
        return Response(status=204)

    return Response(ReviewSerializer(review, context={"request": request}).data)