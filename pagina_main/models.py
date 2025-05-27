from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify
from django.db.models import Avg

class Genre(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Anime(models.Model):
    FORMAT_CHOICES = [
        ('TV', 'TV'),
        ('Movie', 'Movie'),
        ('OVA', 'OVA'),
        ('ONA', 'ONA'),
        ('Special', 'Special'),
    ]
    STATUS_CHOICES = [
        ('airing', 'Airing'),
        ('finished', 'Finished'),
        ('upcoming', 'Upcoming'),
    ]

    title       = models.CharField(max_length=200)
    description = models.TextField(max_length=500, blank=True)
    slug        = models.SlugField(unique=True, blank=True)
    genres      = models.ManyToManyField(Genre, blank=True)
    image       = models.URLField(blank=True, default="https://via.placeholder.com/150")
    format      = models.CharField(max_length=20, choices=FORMAT_CHOICES)
    status      = models.CharField(max_length=20, choices=STATUS_CHOICES)
    episodes    = models.PositiveIntegerField()
    year        = models.DateField()
    is_trending = models.BooleanField(default=False)
    is_seasonal = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    @property
    def aggregate_avg_score(self):
        """
        Devuelve la puntuación media redondeada a 2 decimales
        """
        agg = self.user_animes.exclude(score__isnull=True).aggregate(avg=Avg('score'))['avg']
        return round(agg or 0, 2)

    def __str__(self):
        return self.title

STATUS_CHOICES = [
    ('pending',   'Planeado para ver'),
    ('watching',  'Viéndolo'),
    ('paused',    'En pausa'),
    ('dropped',   'Dropeado'),
    ('completed', 'Finalizado'),
]

class Profile(models.Model):
    user   = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)

    def __str__(self):
        return self.user.username

class UserAnime(models.Model):
    """
    Relaciona usuarios y animes, con estado y puntuación.
    """
    user      = models.ForeignKey(User, on_delete=models.CASCADE)
    anime     = models.ForeignKey(Anime, on_delete=models.CASCADE, related_name='user_animes')
    status    = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    score     = models.PositiveSmallIntegerField(null=True, blank=True)
    added_at  = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'anime')

    def __str__(self):
        return f"{self.user.username} – {self.anime.title} ({self.get_status_display()})"