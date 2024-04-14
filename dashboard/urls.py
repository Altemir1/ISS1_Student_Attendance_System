from django.urls import path
from . import views
from django.views.generic import RedirectView

app_name = 'dashboard'
urlpatterns = [
    #STUDENT
    path('', RedirectView.as_view(url='/account/login/')),
    path('student_profile/', views.student_profile, name='student_profile'),
    path('student_courses/', views.student_courses, name='student_courses'),
    path('student_courses_specific_one/<str:course_code>/', views.student_courses_specific_one, name='student_courses_specific_one'),
    path('student_document_submission/',views.student_document_submission, name='student_document_submission'),
    #TEACHER
    path('specific_course/<str:course_code>/<str:course_type>/', views.teacher_course_displayer, name='teacher_course_displayer'),
]