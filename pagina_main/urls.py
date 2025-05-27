from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views
from .views import AnimeViewSet, UserAnimeViewSet  # <-- IMPORTANTE

app_name = 'anime'

router = DefaultRouter()
router.register(r'animes', AnimeViewSet, basename='anime')
router.register(r'ratings', UserAnimeViewSet, basename='rating')

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('list/', views.anime_index, name='index'),
    path('profile/', views.profile_view, name='profile'),
    path('search/', views.anime_search, name='anime_search'),
    path('<slug:slug>/', views.anime_detail, name='detail'),
    path('api/', include(router.urls)),  # <-- Necesario para acceder a /api/animes y /api/ratings
]
