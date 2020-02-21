from django.urls import path
from apps.cms import views

app_name = 'cms'

urlpatterns = [
    path('', views.index, name='index'),
    path('write_news/', views.WriteNews.as_view(), name='write_news'),
    path('news_category/', views.news_category, name='news_category'),
    path('login/', views.login_view, name='login')
]