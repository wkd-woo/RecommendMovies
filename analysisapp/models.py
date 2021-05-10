from django.db import models

# Create your models here.

class ratings(models.Model): # 평점 모델.
    #user_id #user_id, foreignkey
    rating_id = models.IntegerField(primary_key=True, auto_created=True) # rating_id, pk
    rating = models.FloatField() # 평점
    movie_id = models.ForeignKey() # DB에 있는 movies 연동. foreignKey

    def __init__(self):
        self




#class RateManager():

   # def insert_rating(self, user_id, movie_id, rating):
