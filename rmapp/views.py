from django.shortcuts import render

# Create your views here.
def home(request):
    context = {

    }
    return render(request, 'rmapp/home.html', context)

def about(request):
    context = {

    }
    return render(request, 'rmapp/aboutus.html', context)