from django.db import models

# Create your models here.

class Movie(models.Model):
    movieId = models.CharField(max_length=50, primary_key=True) # 영화 id
    title = models.CharField(max_length=50) # 영화 제목
    genres = models.CharField(max_length=300, null=True)    # 영화 장르
    imgurl = models.CharField(max_length=300, null=True)    # 영화 포스터
