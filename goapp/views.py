from django.shortcuts import render

# Create your views here.
def recommend(request):
    context = {

    }
    return render(request, 'goapp/recommend.html', context)

def rating(request):
    context = {

    }
    return render(request, 'goapp/rating.html', context)