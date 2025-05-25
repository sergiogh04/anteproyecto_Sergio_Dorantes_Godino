from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.http import JsonResponse
from django.db.models import Q

from .forms import UserRegisterForm
from .models import Anime, STATUS_CHOICES, UserAnime, Profile

def home(request):
    return render(request, 'home.html')

def register_view(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('anime:home')
    else:
        form = UserRegisterForm()
    return render(request, 'registration/register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('anime:home')
    else:
        form = AuthenticationForm()
    return render(request, 'registration/login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('anime:home')

@login_required(login_url='anime:login')
def anime_index(request):
    trending = Anime.objects.filter(is_trending=True)
    seasonal = Anime.objects.filter(is_seasonal=True)
    return render(request, 'pag_main/index.html', {
        'trending': trending,
        'seasonal': seasonal,
    })

@login_required(login_url='anime:login')
def anime_detail(request, slug):
    anime = get_object_or_404(Anime, slug=slug)

    # Procesar formulario de añadir a lista
    if request.method == 'POST':
        status = request.POST.get('status')
        ua, created = UserAnime.objects.get_or_create(user=request.user, anime=anime)
        ua.status = status
        ua.save()
        return redirect('anime:detail', slug=slug)

    user_anime = UserAnime.objects.filter(user=request.user, anime=anime).first()

    return render(request, 'pag_main/anime_details.html', {
        'anime': anime,
        'status_choices': STATUS_CHOICES,
        'user_anime': user_anime,
    })

@login_required(login_url='anime:login')
def profile_view(request):
    profile, _ = Profile.objects.get_or_create(user=request.user)
    user_list = UserAnime.objects.filter(user=request.user).select_related('anime')
    grouped = [
        (code, label, user_list.filter(status=code))
        for code, label in STATUS_CHOICES
    ]
    return render(request, 'user_profile/profile.html', {
        'profile': profile,
        'grouped_animes': grouped,
        'status_choices': STATUS_CHOICES,
    })

def anime_search(request):
    q = request.GET.get('q', '').strip()
    results = []
    if q:
        qs = Anime.objects.filter(Q(title__icontains=q))[:10]
        for anime in qs:
            results.append({
                'slug': anime.slug,
                'title': anime.title,
                'image': anime.image,  # URLField
            })
    return JsonResponse({'results': results})