from django.shortcuts import HttpResponse, render
from .models import Movie
import csv
import pandas as pd
from analysisapp.models import Results
from django.core.paginator import Paginator

# Create your views here.

def recommend(request):
    qs = Results.pdobjects.all()
    rating_predictions = qs.to_dataframe()


    context = {
    }
    return render(request, 'goapp/recommend.html', context)


def rating_home(request):
    poster_moviePath = 'goapp/data/poster_movies.csv'
    poster_movieFile = open(poster_moviePath, 'r', encoding='ISO-8859-1')
    poster_movieReader = csv.reader(poster_movieFile)
    print('-------', poster_movieReader)
    """list = []
    for row in poster_movieReader:
        list.append(Movie(movieId=row[1],
                          title=row[2],
                          genres=row[3],
                          imgurl=row[4]))
    Movie.objects.bulk_create(list)

    return HttpResponse('create model ')"""
    """movie_list = Movie.objects.all().filter(imgurl__contains='/')[:30]
    # Movie 모델의 imgurl모델에서 '/'문자열을 포함하는 30개의 데이터 조회
    context = {
        'movie_list': movie_list
    }"""
    # 입력 파라미터
    page = request.GET.get('page', '1') # 페이지

    # 조회
    movie_list = Movie.objects.all()[1:]

    # 페이징처리
    paginator = Paginator(movie_list, 30)  # 페이지당 10개씩 보여주기
    page_obj = paginator.get_page(page)
    context = {
        'movie_list': page_obj
    }
    # 저장된 모든 영화 불러오기
    return render(request, 'goapp/rating.html', context)

def rating_detail(request, movie_id):
    movie = Movie.objects.get(movieId=movie_id)
    context = {
        'movie':movie
    }
    return render(request, 'goapp/rating_detail.html', context)
