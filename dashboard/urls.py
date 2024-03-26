from django.urls import path
from . import views

app_name = 'dashboard'
urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('course_dashboard/<int:course_id>/<str:teacher_id>/', views.course_dashboard, name='course_dashboard'),
     
]