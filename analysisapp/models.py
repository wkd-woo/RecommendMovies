from django.contrib.auth.models import User
from django.db import models


# Create your models here.

class Rating(models.Model):  # 평점 모델.
    rating_id = models.AutoField(primary_key=True)  # rating_gid, pk
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)  # 내부 DB에 있는 USER 연동. foreignKey
    movie_id = models.IntegerField()  # 외부 DB에 있는 movies 연동. foreignKey
    rating = models.FloatField(default=2.5, verbose_name='평점')  # 평점
    timestamp = models.DateTimeField(auto_now_add=True)  # 해당 레코드 생성시 현재 시간 자동 저장
    comment = models.CharField(max_length=240, verbose_name='코멘트', help_text='코멘트를 입력해 주세요. 240자 제한.', null=True)  # 240자 제한


def rateManager(self, user_id, movie_id, rating, comment):
    """
    평점 모델 manager
    """

    def insert_rating(self, r_model, user_id, movie_id, rating, comment):
        # 테이블 입력
        r_model.user_id = user_id
        r_model.movie_id = movie_id
        r_model.rating = rating
        r_model.comment = comment
        return r_model

    insertedRate = Rating() # model 생성 후
    insertedRate = insert_rating(insertedRate, user_id, movie_id, rating, comment) # 테이블 입력!
    return insertedRate # 반환
