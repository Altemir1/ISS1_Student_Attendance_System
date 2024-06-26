from django.urls import path
from . import views

app_name = 'attendance'
urlpatterns = [
    path('att_toggle/<str:att_id>/<str:course_code>/<str:group>/<str:course_type>/', views.att_toggle, name='att_toggle'),
    path('open_registration/<str:course_code>/<str:group>/<str:course_type>/', views.open_registration, name='open_registration'),
    path('manual_attendance/<str:course_code>/<str:is_lecture>/',views.manual_attendance,name='manual_attendance'),
    path('card_reader/',views.card_reader,name='card_reader'),
    path('reset_everything/',views.reset_everything,name='reset_everything'),
]