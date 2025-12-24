# backend/recommends/urls.py
from django.urls import path
from . import views

urlpatterns = [
  path("ai/", views.ai_taste),  
  path("genres/", views.genre_recommend),
  path("people/", views.people_recommend),
  path("users/", views.user_recommend),
  path("taste/", views.taste_summary),
]

