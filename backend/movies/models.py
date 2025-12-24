# backend/movies/models.py
from django.db import models
from django.conf import settings


class Genre(models.Model):
    tmdb_id = models.PositiveIntegerField(unique=True)
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Person(models.Model):
    tmdb_id = models.PositiveIntegerField(unique=True)
    name = models.CharField(max_length=100)
    profile_path = models.CharField(max_length=255, blank=True)
    known_for_department = models.CharField(max_length=50, blank=True)

    def __str__(self):
        return self.name


class Movie(models.Model):
    tmdb_id = models.PositiveIntegerField(unique=True)

    title = models.CharField(max_length=200)
    original_title = models.CharField(max_length=200, blank=True)

    overview = models.TextField(blank=True)
    release_date = models.DateField(null=True, blank=True)

    poster_path = models.CharField(max_length=255, blank=True)
    backdrop_path = models.CharField(max_length=255, blank=True)

    popularity = models.FloatField(default=0)
    vote_average = models.FloatField(default=0)
    vote_count = models.PositiveIntegerField(default=0)

    runtime = models.PositiveIntegerField(null=True, blank=True)  # 상세에서만 채워질 수 있음

    genres = models.ManyToManyField(Genre, through="MovieGenre", related_name="movies")
    people = models.ManyToManyField(Person, through="MovieCredit", related_name="movies")

    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class MovieGenre(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["movie", "genre"], name="unique_movie_genre")
        ]


class MovieCredit(models.Model):
    ROLE_CHOICES = [
        ("DIRECTOR", "Director"),
        ("CAST", "Cast"),
    ]

    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    person = models.ForeignKey(Person, on_delete=models.CASCADE)

    role_type = models.CharField(max_length=20, choices=ROLE_CHOICES)
    character_name = models.CharField(max_length=100, blank=True)  # cast
    job = models.CharField(max_length=50, blank=True)              # crew
    order = models.IntegerField(default=0)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["movie", "person", "role_type"], name="unique_credit")
        ]


class HomeSectionEntry(models.Model):
    SECTION_CHOICES = [
        ("POPULAR", "Popular"),
        ("NOW_PLAYING", "Now Playing"),
        ("TOP_RATED", "Top Rated"),
    ]
    section = models.CharField(max_length=20, choices=SECTION_CHOICES)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name="home_entries")
    rank = models.PositiveIntegerField(default=0)
    synced_at = models.DateTimeField(auto_now=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["section", "movie"], name="unique_section_movie")
        ]
        ordering = ["rank"]






# 마이페이지 

class PersonLike(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="person_likes")
    person = models.ForeignKey(Person, on_delete=models.CASCADE, related_name="likes")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["user", "person"], name="unique_user_person_like")
        ]

class GenreLike(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="genre_likes")
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE, related_name="likes")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["user", "genre"], name="unique_user_genre_like")
        ]
        
        
        



# 영화 상세 
class MovieLike(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="movie_likes")
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name="likes")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["user", "movie"], name="unique_user_movie_like")
        ]
        
        
        
    

# 인물 좋아요 저장 모델
class LikedPerson(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='liked_people')
    person_id = models.IntegerField()  # TMDB 인물 ID
    name = models.CharField(max_length=100)
    profile_path = models.CharField(max_length=200, null=True, blank=True)
    department = models.CharField(max_length=50, null=True, blank=True) # 직업(Acting 등)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'person_id') # 중복 좋아요 방지
        