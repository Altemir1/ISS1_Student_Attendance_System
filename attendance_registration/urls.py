from django.urls import path
from .views import register_attendance

app_name = 'attendance_registration'
urlpatterns = [
    path('register/',register_attendance, name='register_attendance'),
]