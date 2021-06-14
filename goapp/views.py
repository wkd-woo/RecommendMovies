from django.shortcuts import HttpResponse, render, redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView
from analysisapp.forms import ResultsCreationForm
from analysisapp.predict import *
from .models import Movie
import csv
import pandas as pd
from analysisapp.models import Rating
from django.core.paginator import Paginator
from .froms import RatingForm

# Create your views here.


class recommendResultObject():
    objects = goRecommend()
    PredictDataFrame = objects.Predict(1003)  # userId로 변경가능!!!!

    Top12 = guessYouLikeIt(PredictDataFrame, 1003)
    Worst12 = guessYouHateIt(PredictDataFrame, 1003)
    Action = genreThatYouLike(PredictDataFrame, 1003, 1)
    Romance = genreThatYouLike(PredictDataFrame, 1003, 15)


def recommend(request):
    result = recommendResultObject

    Mlist = []
    Mstar = []
    Wlist = []
    Wstar = []
    Alist = []
    Astar = []
    Rlist = []
    Rstar = []
    for id, star in result.Top12.items():
        Mlist.append(Movie.objects.get(movieId=id))
        Mstar.append(round(star, 2))    # 소수점 두 번째 까지

    for id, star in result.Worst12.items():
        Wlist.append(Movie.objects.get(movieId=id))
        Wstar.append(round(star, 2))

    for id, star in result.Action.items():
        Alist.append(Movie.objects.get(movieId=id))
        Astar.append(round(star, 2))

    for id, star in result.Romance.items():
        Rlist.append(Movie.objects.get(movieId=id))
        Rstar.append(round(star, 2))

    #=======> 효율적으로 만드는 방법이 없을까
    """
    def getModel(dic):
        for id, star in dic.items():
            dic.append(Movie.objects.get(movieId=id))
            dic.append(star)
    """
    #========<

    context = {
        'Mlist':Mlist,
        'Mstar':Mstar,
        'Wlist':Wlist,
        'Wstar':Wstar,
        'Alist':Alist,
        'Astar':Astar,
        'Rlist':Rlist,
        'Rstar':Rstar
    }
    return render(request, 'goapp/recommend.html', context)


def rating_home(request):
    poster_moviePath = 'goapp/data/poster_movies.csv'
    poster_movieFile = open(poster_moviePath, 'r', encoding='ISO-8859-1')
    poster_movieReader = csv.reader(poster_movieFile)
    print('-------', poster_movieReader)

#======================================
    def ormMovieImport():
        list = []
        for row in poster_movieReader:
            list.append(Movie(movieId=row[1],
                              title=row[2],
                              genres=row[3],
                              imgurl=row[4]))
        Movie.objects.bulk_create(list)

        return HttpResponse('create model ')
        movie_list = Movie.objects.all().filter(imgurl__contains='/')[:30]
        # Movie 모델의 imgurl모델에서 '/'문자열을 포함하는 30개의 데이터 조회
        context = {
            'movie_list': movie_list
        }
#=======================================


    # 입력 파라미터
    page = request.GET.get('page', '1') # 페이지

    # 조회
    movie_list = Movie.objects.all()[1:]

    # 검색어 가져오기
    search_key = request.GET.get('search_key')
    if search_key:
        movie_list = Movie.objects.all().filter(title__icontains=search_key) # 해당 검색어를 포함한 queryset 가져오기

    # 페이징처리
    paginator = Paginator(movie_list, 30)  # 페이지당 30개씩 보여주기
    page_obj = paginator.get_page(page)
    print(page_obj)
    context = {
        'movie_list': page_obj,
        'search_key': search_key
    }
    # 저장된 모든 영화 불러오기
    return render(request, 'goapp/rating.html', context)

def rating_detail(request, movie_Id):
    movie = Movie.objects.get(movieId=movie_Id) # movieId가 movie_id인 행을 movie에 가져옴
    form = RatingForm(request.POST, request.FILES)
    if request.method == 'POST':
        if form.is_valid():
            ratingM = form.save(commit=False)
            ratingM.user_id = request.user
            ratingM.movie_id = movie_Id
            form.save()

    context = {
        'movie':movie,
        'form':form
    }
    return render(request, 'goapp/rating_detail.html', context)

