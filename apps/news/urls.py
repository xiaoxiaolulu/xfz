from django.urls import path
from apps.news import views

app_name = 'news'

urlpatterns = [
    path('', views.index, name='index'),
    path('detail/<int:news_id>/', views.news_detail, name='news_detail'),
    path('search/', views.search, name='search'),
    path('list/', views.new_list, name='list'),
    path('public_comment/', views.public_comment, name='public_comment'),
]
