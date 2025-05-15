from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import User


class Anime(models.Model):
    STATUS_CHOICES = [
        ('airing', 'En Emisión'),
        ('finished', 'Finalizado'),
        ('upcoming', 'Próximamente'),
    ]

    title = models.CharField(max_length=200)
    description = models.TextField()
    cover_image = models.ImageField(upload_to='anime_covers/')
    categories = models.CharField(max_length=200)
    episodes = models.PositiveIntegerField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES)
    rating = models.FloatField(default=0.0)
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class Review(models.Model):
    RATING_CHOICES = [(i, str(i)) for i in range(1, 6)]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    anime = models.ForeignKey(Anime, on_delete=models.CASCADE)
    rating = models.IntegerField(choices=RATING_CHOICES)
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'anime')


class UserAnimeList(models.Model):
    LIST_CHOICES = [
        ('watching', 'Viendo'),
        ('planned', 'Planeado'),
        ('completed', 'Completado'),
        ('dropped', 'Abandonado'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    anime = models.ForeignKey(Anime, on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=LIST_CHOICES)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('user', 'anime')