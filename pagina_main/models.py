from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


#MODELOS DE PAGINA DE INICIO

# MODELOS DE PERFILES DE USUARIO



#MODELOS DE LA PAGINA PRINCIPAL

from django.db import models
from django.utils.text import slugify

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
    title = models.CharField(max_length=200)
    description = models.TextField(max_length=500, blank=True)
    slug = models.SlugField(unique=True, blank=True)
    genres = models.ManyToManyField(Genre, blank=True)
    image = models.URLField(blank=True, default="https://via.placeholder.com/150")
    format = models.CharField(max_length=20, choices=FORMAT_CHOICES)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES)
    episodes = models.PositiveIntegerField()
    year = models.DateField()
    is_trending = models.BooleanField(default=False)
    is_seasonal = models.BooleanField(default=False)


    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title
from django.contrib.auth.models import User

STATUS_CHOICES = [
    ('pending',   'Planeado para ver'),
    ('watching',  'Viéndolo'),
    ('paused',    'En pausa'),
    ('dropped',   'Dropeado'),
    ('completed', 'Finalizado'),
]

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)

    def __str__(self):
        return self.user.username

class UserAnime(models.Model):
    user   = models.ForeignKey(User, on_delete=models.CASCADE)
    anime  = models.ForeignKey(Anime, on_delete=models.CASCADE)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    added_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'anime')

    def __str__(self):
        return f"{self.user.username} – {self.anime.title} ({self.get_status_display()})"


# MODELOS DE DETALLES DE UN ANIME


# MODELOS DE DETALLES DE UNA NOTICIA

