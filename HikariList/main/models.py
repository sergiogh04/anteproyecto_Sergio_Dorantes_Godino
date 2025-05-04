from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Genre(models.Model):
    name = models.CharField(max_length=50, unique=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name

class Studio(models.Model):
    name = models.CharField(max_length=100)
    founded = models.DateField()
    website = models.URLField(blank=True)

    def __str__(self):
        return self.name

class Anime(models.Model):
    STATUS_CHOICES = [
        ('ongoing', 'En Emisión'),
        ('finished', 'Finalizado'),
        ('upcoming', 'Próximamente'),
    ]

    title = models.CharField(max_length=200)
    synopsis = models.TextField()
    genres = models.ManyToManyField(Genre)
    studio = models.ForeignKey(Studio, on_delete=models.SET_NULL, null=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES)
    episodes = models.PositiveIntegerField()
    release_date = models.DateField()
    rating = models.FloatField(default=0.0)
    poster = models.ImageField(upload_to='posters/')
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def update_rating(self):
        reviews = self.reviews.all()
        if reviews:
            self.rating = sum([review.rating for review in reviews]) / len(reviews)
            self.save()

    def __str__(self):
        return self.title

class Review(models.Model):
    RATING_CHOICES = [(i, str(i)) for i in range(1, 11)]
    anime = models.ForeignKey(Anime, related_name='reviews', on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.IntegerField(choices=RATING_CHOICES)
    comment = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('anime', 'user')
