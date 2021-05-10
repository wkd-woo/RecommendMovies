from django.urls import path

from . import views

app_name = 'goapp'

urlpatterns = [
    path('', views.recommend, name='recommend'),
    path('rating/', views.rating, name='rating'),
]