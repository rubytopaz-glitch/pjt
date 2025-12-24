from django.contrib import admin
from .models import Movie, Genre, Person, MovieGenre, MovieCredit, HomeSectionEntry


@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    list_display = ("id", "tmdb_id", "title", "vote_average", "popularity", "updated_at")
    search_fields = ("title", "original_title")


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ("id", "tmdb_id", "name")
    search_fields = ("name",)


@admin.register(Person)
class PersonAdmin(admin.ModelAdmin):
    list_display = ("id", "tmdb_id", "name", "known_for_department")
    search_fields = ("name",)


admin.site.register(MovieGenre)
admin.site.register(MovieCredit)
admin.site.register(HomeSectionEntry)
