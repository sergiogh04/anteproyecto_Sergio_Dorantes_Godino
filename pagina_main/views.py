from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.db.models import Q, Avg
from rest_framework import viewsets, permissions
from .models import Anime, STATUS_CHOICES, UserAnime, Profile, Genre
from .forms import UserRegisterForm
from .serializers import AnimeSerializer, UserAnimeSerializer

# Vistas de la aplicación (HTML)

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
    top_rated = Anime.objects.annotate(avg=Avg('user_animes__score')) \
                     .filter(avg__isnull=False) \
                     .order_by('-avg')[:12]
    return render(request, 'pag_main/index.html', {
        'trending': trending,
        'seasonal': seasonal,
        'top_rated': top_rated,
    })


@login_required(login_url='anime:login')
def anime_detail(request, slug):
    anime = get_object_or_404(Anime, slug=slug)
    user_anime = None

    if request.user.is_authenticated:
        user_anime, _ = UserAnime.objects.get_or_create(user=request.user, anime=anime)
        if request.method == 'POST':
            status = request.POST.get('status')
            if status in dict(STATUS_CHOICES):
                user_anime.status = status
            score = request.POST.get('score')
            if score and score.isdigit() and 1 <= int(score) <= 10:
                user_anime.score = int(score)
            user_anime.save()
            return redirect('anime:detail', slug=slug)

    avg_score = UserAnime.objects.filter(anime=anime, score__isnull=False) \
                .aggregate(avg=Avg('score'))['avg']

    return render(request, 'pag_main/anime_details.html', {
        'anime': anime,
        'user_anime': user_anime,
        'status_choices': STATUS_CHOICES,
        'avg_score': round(avg_score, 2) if avg_score else None,
        'score_range': range(1, 11),  # Para el selector de puntuación
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
            results.append({'slug': anime.slug, 'title': anime.title, 'image': anime.image})
    return JsonResponse({'results': results})


#api
class AnimeViewSet(viewsets.ReadOnlyModelViewSet):

    queryset = Anime.objects.all()
    serializer_class = AnimeSerializer
    lookup_field = 'slug'

    def get_queryset(self):
        qs = super().get_queryset()
        if self.request.query_params.get('ordering') == 'top':
            qs = qs.annotate(avg=Avg('user_animes__score')) \
                   .filter(avg__isnull=False) \
                   .order_by('-avg')
        return qs


class UserAnimeViewSet(viewsets.ModelViewSet):

    queryset = UserAnime.objects.all()
    serializer_class = UserAnimeSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)
