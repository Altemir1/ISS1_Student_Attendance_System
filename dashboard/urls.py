from django.urls import path
from . import views

app_name = 'dashboard'
urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('specific_course/<int:course_code>/<str:id>/', views.specific_course, name='specific_course'),
    path('specific_course/', views.certificate_submission ,name='certificate_submission'),
]