from django.urls import path

from .views import candidate_suggestions, candidate_opinion, candidate_note

urlpatterns = [
    path('suggestions/', candidate_suggestions),
    path('opinion', candidate_opinion),
    path('<str:candidate_id>/note', candidate_note)
]
