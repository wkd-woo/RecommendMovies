from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
# Create your models here.

class Movie(models.Model):
    movieId = models.CharField(max_length=50, primary_key=True) # 영화 id
    title = models.CharField(max_length=50) # 영화 제목
    genres = models.CharField(max_length=300, null=True)    # 영화 장르
    imgurl = models.CharField(max_length=300, null=True)    # 영화 포스터


class RatingStar(models.Model):
    movieId = models.CharField(max_length=50)
    starscore = models.IntegerField(default=0,
        validators=[
            MaxValueValidator(5),
            MinValueValidator(0)
        ]
    )    # 별점
    # 문자 표현 제공
    def __str__(self):
        return str(self.pk)