from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from animes.models import Anime, Studio, Genre


# Create your views here.
@login_required
def index(request):
    animes = Anime.objects.all()
    context = {'animes' : animes}
    return render(request, 'animes/index.html', context)

@login_required
def anime_details(request, anime_id):
    anime = Anime.objects.get(pk=anime_id)
    context = {'anime' : anime}
    return render(request, 'animes/anime_details.html', context)

@login_required
def studio_list(request):
    studios = Studio.objects.all()
    context = {'studios' : studios}
    return render(request, 'animes/studio_list.html', context)
@login_required
def studio_details(request, studio_id):
    studio = Studio.objects.get(pk=studio_id)
    context = {'studio' : studio}
    return render(request, 'animes/studio_details.html', context)

@login_required
def genre_list(request):
    genres = Genre.objects.all()
    context = {'genres' : genres}
    return render(request, 'animes/genre_list.html', context)
