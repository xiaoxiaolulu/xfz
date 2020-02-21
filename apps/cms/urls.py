from django.urls import path
from apps.cms import views

app_name = 'cms'

urlpatterns = [
    path('login/', views.login_view, name='login')
]