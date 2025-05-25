# yourapp/urls.py
from django.urls import path
from . import views

app_name = 'anime'

urlpatterns = [
    path('', views.home, name='home'),  # Portada
    path('register/', views.register_view, name='register'),  # Registro de usuario
    path('login/', views.login_view, name='login'),           # Inicio de sesión
    path('logout/', views.logout_view, name='logout'),        # Cerrar sesión
    path('list/', views.anime_index, name='index'),           # Lista de animes (/list/)
    path('profile/', views.profile_view, name='profile'),
    path('search/', views.anime_search, name='anime_search'),
    path('<slug:slug>/', views.anime_detail, name='detail'),  # Detalle de anime

]
