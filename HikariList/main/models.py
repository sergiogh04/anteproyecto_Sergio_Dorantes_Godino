from django.db import models
from django.contrib.auth.models import User

class Genre(models.Model):
    name = models.CharField(max_length=50)

class Anime(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    episodes = models.PositiveIntegerField()
    genres = models.ManyToManyField(Genre)
    cover_image = models.ImageField(upload_to='covers/')
    created_at = models.DateTimeField(auto_now_add=True)

STATUS_CHOICES = [
    ('W', 'Watching'),
    ('C', 'Completed'),
    ('O', 'On Hold'),
    ('D', 'Dropped'),
    ('P', 'Plan to Watch'),
]

class UserAnimeList(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    anime = models.ForeignKey(Anime, on_delete=models.CASCADE)
    status = models.CharField(max_length=1, choices=STATUS_CHOICES)
    rating = models.PositiveSmallIntegerField(null=True, blank=True)
    review = models.TextField(blank=True)
    watched_episodes = models.PositiveIntegerField(default=0)