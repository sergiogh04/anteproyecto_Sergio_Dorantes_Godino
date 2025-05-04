from django.views.generic import ListView, DetailView, CreateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from .models import Anime, Review
from .forms import AnimeForm, ReviewForm

class AnimeListView(ListView):
    model = Anime
    template_name = 'anime/list.html'
    paginate_by = 20
    context_object_name = 'animes'

    def get_queryset(self):
        queryset = super().get_queryset()
        genre = self.request.GET.get('genre')
        if genre:
            queryset = queryset.filter(genres__name=genre)
        return queryset.order_by('-created_at')

class AnimeDetailView(DetailView):
    model = Anime
    template_name = 'anime/detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['review_form'] = ReviewForm()
        return context

class AnimeCreateView(LoginRequiredMixin, CreateView):
    model = Anime
    form_class = AnimeForm
    template_name = 'anime/form.html'

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('anime-detail', kwargs={'pk': self.object.pk})
