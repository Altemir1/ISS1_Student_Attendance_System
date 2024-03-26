from django.urls import path
from . import views

app_name = 'attendance'
urlpatterns = [
    path('student_att/<int:course_id>/<str:student_id>/', views.student_att, name='student_att'),
]