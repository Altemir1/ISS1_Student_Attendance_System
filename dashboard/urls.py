from django.urls import path
from . import views

app_name = 'dashboard'
urlpatterns = [
    path('', views.dashboard, name='dashboard'),
     path('course_dashboard/<int:course_id>/<str:teacher_id>/', views.course_dashboard, name='course_dashboard'),
     path('student_att/<int:course_id>/<str:student_id>/', views.student_att, name='student_att'),
     
]