from django.db import models

# Create your models here.

class Studio(models.Model):
    name = models.CharField(max_length=200)
    foundation_year = models.DateField()
    country = models.CharField(max_length=200)
    def __str__(self):
        return self.name


class Anime(models.Model):
    title = models.CharField(max_length=200)
    studio = models.ForeignKey(Studio, on_delete=models.CASCADE)
    genre =  models.ForeignKey('Genre', on_delete = models.CASCADE)
    release_date =  models.DateField()
    episodes = models.CharField(max_length=4)
    synopsis = models.TextField()
    def __str__(self):
        return self.title



class Genre(models.Model):

    genre_name = models.CharField(max_length = 200)
    genre_description  = models.TextField()
    def __str__(self):
        return self.genre_name
