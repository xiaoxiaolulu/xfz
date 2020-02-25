from django.urls import path
from apps.course import views

app_name = 'course'

urlpatterns = [
    path('', views.course_index, name='course_index'),
    path('detail/<int:course_id>', views.course_detail, name='course_detail'),
    path('course_token/', views.course_token, name='course_token'),
    path('course_order/<int:course_id>/', views.course_order, name='course_order')
]
