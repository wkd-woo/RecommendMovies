from django.urls import path

from . import views

app_name = 'goapp'

urlpatterns = [
    path('', views.recommend, name='recommend'),
    path('rating/', views.rating_home, name='rating_home'),
    path('<str:movie_Id>/', views.rating_detail, name='rating_detail'),
]