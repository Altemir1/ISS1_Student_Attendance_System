from django.urls import path
from . import views

app_name = 'attendance'
urlpatterns = [
    path('att_toggle/<str:att_id>/<str:course_code>/<str:group>/<str:course_type>/', views.att_toggle, name='att_toggle'),
]