from django.shortcuts import HttpResponse, render
from .models import Movie
from analysisapp.models import Results, Rating
import csv

"""import pandas as pd
# 프로젝트 root를 import 참조 경로에 추가
import os, sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
from analysisapp.predict import goRecommend
"""


# Create your views here.

def recommend(request):     # go/ url view
    qs = Results.rsobject.all() # Use the Pandas Manager
    rating_predictions = qs.to_dataframe()

    context = {

    }
    return render(request, 'goapp/recommend.html', context)


def rating_home(request):   # go/rating/ url view
    poster_moviePath = 'goapp/data/poster_movies.csv'   # csv 파일 경로
    poster_movieFile = open(poster_moviePath, 'r', encoding='ISO-8859-1')   # csv 파일을 읽기 모드로 열기
    poster_movieReader = csv.reader(poster_movieFile)   #  csv 파일을 읽어오기
    print('-------', poster_movieReader)    # 준비되면 출력
    """ csv파일을 model 데이터 삽입
    list = []
    for row in poster_movieReader:
        list.append(Movie(movieId=row[1],
                          title=row[2],
                          genres=row[3],
                          imgurl=row[4]))
    Movie.objects.bulk_create(list)

    return HttpResponse('create model ')"""
    movie_list = Movie.objects.all().filter(imgurl__contains='/')[:30]
    # Movie 모델의 imgurl모델에서 '/'문자열을 포함하는 30개의 데이터 조회

    context = {
        'movie_list': movie_list
    }
    return render(request, 'goapp/rating.html', context)
