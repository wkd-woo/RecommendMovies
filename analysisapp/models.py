from django.contrib.auth.models import User
from django.db import models


# Create your models here.

class ratings(models.Model): # 평점 모델.
    rating_id = models.AutoField(primary_key=True) # rating_gid, pk
    user_id = models.ForeignKey(User, on_delete=models.CASCADE) # 내부 DB에 있는 USER 연동. foreignKey
    #movie_id = models.ForeignKey() # 외부 DB에 있는 movies 연동. foreignKey
    rating = models.FloatField(default=2.5) # 평점



#class RateManager():
   # def insert_rating(self, user_id, movie_id, rating):
