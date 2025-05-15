from django.urls import path
from .views import AnimeListView, AnimeDetailView, AddReviewView, UpdateListStatus

urlpatterns = [
    path('trending/', AnimeListView.as_view(), name='anime_list'),
    path('anime/<int:pk>/', AnimeDetailView.as_view(), name='anime_detail'),
    path('anime/<int:pk>/review/', AddReviewView.as_view(), name='add_review'),
    path('anime/<int:pk>/update-status/', UpdateListStatus.as_view(), name='update_status'),
]