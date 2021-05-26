from django.db import models

# Create your models here.

class Movie(models.Model):
    movieId = models.CharField(max_length=50, primary_key=True)
    title = models.CharField(max_length=50)
    genres = models.CharField(max_length=300, null=True)
    imgurl = models.CharField(max_length=300, null=True)
