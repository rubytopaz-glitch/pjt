from django.contrib import admin
from .models import Review

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ("id", "movie", "user", "rating", "watched", "created_at")
    search_fields = ("content", "user__username", "movie__title")
