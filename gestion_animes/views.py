from django.db.models import Count
from django.shortcuts import render, redirect

# Create your views here.
from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView, View
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Anime, Review, UserAnimeList
from .forms import ReviewForm


class AnimeListView(ListView):
    model = Anime
    template_name = 'anime_list.html'
    context_object_name = 'animes'
    paginate_by = 12

    def get_queryset(self):
        return Anime.objects.order_by('-rating')[:50]


class AnimeDetailView(DetailView):
    model = Anime
    template_name = 'anime_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['reviews'] = Review.objects.filter(anime=self.object)
        context['form'] = ReviewForm()
        return context


class AddReviewView(LoginRequiredMixin, View):
    def post(self, request, pk):
        anime = get_object_or_404(Anime, pk=pk)
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.user = request.user
            review.anime = anime
            review.save()
            return redirect('anime_detail', pk=pk)
        return render(request, 'anime_detail.html', {'form': form})


class UpdateListStatus(LoginRequiredMixin, View):
    def post(self, request, pk):
        anime = get_object_or_404(Anime, pk=pk)
        status = request.POST.get('status')

        UserAnimeList.objects.update_or_create(
            user=request.user,
            anime=anime,
            defaults={'status': status}
        )
        return redirect('anime_detail', pk=pk)


class AnimeList(ListView):
    model = Anime
    template_name = 'anime_list.html'
    context_object_name = 'animes'
    paginate_by = 12
    ordering = ['-rating']

    def get_queryset(self):
        # Obtener animes con mejor rating y al menos 5 reseñas
        return Anime.objects.annotate(
            num_reviews=Count('review')
        ).filter(
            num_reviews__gte=5
        ).order_by('-rating')[:50]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Añadir animes populares adicionales
        context['popular_animes'] = Anime.objects.order_by('-created_at')[:8]
        return context