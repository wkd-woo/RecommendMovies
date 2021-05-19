from django.shortcuts import HttpResponse, render
from .models import Movie
import csv
# Create your views here.
def recommend(request):
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

    context ={
        Movie.objects.get(30)
    }
    return render(request, 'goapp/rating.html', context)