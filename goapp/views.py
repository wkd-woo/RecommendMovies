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
        Mstar.append(star)

    for id, star in result.Worst12.items():
        Wlist.append(Movie.objects.get(movieId=id))
        Wstar.append(star)

    for id, star in result.Action.items():
        Alist.append(Movie.objects.get(movieId=id))
        Astar.append(star)

    for id, star in result.Romance.items():
        Rlist.append(Movie.objects.get(movieId=id))
        Rstar.append(star)

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

    # 페이징처리
    paginator = Paginator(movie_list, 30)  # 페이지당 30개씩 보여주기
    page_obj = paginator.get_page(page)
    context = {
        'movie_list': page_obj
    }
    # 저장된 모든 영화 불러오기
    return render(request, 'goapp/rating.html', context)

def rating_detail(request, movie_id):
    movie = Movie.objects.get(movieId=movie_id) # movieId가 movie_id인 행을 movie에 가져옴
    # rating = Rating.objects.get(movie_id=movie_id)

    #================= POST 실행 오류 수정 ㅠㅠ
    # Exception Type:	IntegrityError
    # NOT NULL constraint failed: analysisapp_rating.user_id_id

    if request.method == 'POST':    # POST 통신을 통해 데이터베이스에 내용 저장
        try:
            #   rating 모델을 불러와 rate값 저장 ======== 이미 저장되어 있는 경우
            rating = Rating()
            """
            왜 try - except로 작성했을까? - 물어봤음 답변 대기
            https://wayhome25.github.io/django/2017/04/01/django-ep9-crud/
            확인해서 해보자
            csv에 넣으나 db에 넣으나 orm에 넣으나 상관없다
            210604 17:43 지금의 생각
            1. db에 userId movieId 같은거 있는지 조회해서 확인
            2-1. 없다면 create import 
            2-2. 있다면 show
            """
            rating.rating = float(request.POST['ratinginput'])
            # request.POST['~']는 POST form 태그 안에서 지정한 name='~' 즉 name이 ~인 태그 안에서 작성한 내용이 ratepost에 들어가게됨
            rating_instance = Rating.objects.get(movie_id=movie_id)
            rating_instance.rating = rating.rating
            rating_instance.save()
            return redirect('goapp:rating_detail/movie_id')
        except:
            try:
                rating_instance = Rating.objects.get(movie_id = movie_id)
                """
                ??? rating_instance를 어디다가 쓰지?
                """
            except Rating.DoesNotExist:
                rating_instance = None
            rating_instance = Rating(movie_id = movie_id, rating = float(request.POST['ratinginput']))
            rating_instance.save()

    #=================

    context = {
        'movie':movie
    }
    return render(request, 'goapp/rating_detail.html', context)

