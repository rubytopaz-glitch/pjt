from django.conf import settings
from django.db import models


class Review(models.Model):
    """
    '한줄평' = 핵심 활동 데이터
    - watched=True 체크 + rating 필수
    - 한 유저는 한 영화에 1개의 리뷰만(수정 가능)
    """
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="reviews"
    )
    movie = models.ForeignKey(
        "movies.Movie", on_delete=models.CASCADE, related_name="reviews"
    )

    content = models.CharField(max_length=200)
    watched = models.BooleanField(default=False)
    rating = models.PositiveSmallIntegerField()  # 1~5

    likes = models.ManyToManyField(
        settings.AUTH_USER_MODEL, related_name="liked_reviews", blank=True
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["user", "movie"], name="uniq_user_movie_review")
        ]
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.movie.tmdb_id} / {self.user} ({self.rating})"

    @property
    def like_count(self):
        return self.likes.count()
# backend/reviews/models.py

# ... (기존 Review 모델 코드 아래에 추가)

class ReviewComment(models.Model):
    """
    리뷰에 달리는 댓글 (대댓글)
    - review: 어떤 리뷰에 달린 댓글인지
    - user: 누가 썼는지
    - content: 내용
    """
    review = models.ForeignKey(Review, on_delete=models.CASCADE, related_name="comments")
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Reply by {self.user} on Review {self.review.id}"