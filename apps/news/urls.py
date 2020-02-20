from django.urls import path
from apps.news import views

app_name = 'news'

urlpatterns = [
    path('', views.index, name='index')
]