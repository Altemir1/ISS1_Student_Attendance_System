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
    path('student_docuemnt_history/', views.student_document_history ,name='student_document_history'),
    
    path('documents/remove/<int:doc_id>', views.remove_document, name='remove_document'), 
    path('documents/download/<int:doc_id>', views.download_document, name='download_document'),
    
    path('student_documents/<str:doc_name>', views.download_document_admin, name='download_document_admin'),
    
    
    #TEACHER
    path('teacher_profile/', views.teacher_profile, name='teacher_profile'),
    path('teacher_courses/', views.teacher_courses, name="teacher_courses"),
    path('teacher_courses_specific_one/<str:course_code>/<str:course_type>/', views.teacher_courses_specific_one, name='teacher_courses_specific_one'),
    path('teacher_courses_specific_one_attendance/<str:course_code>/<str:group>/<str:course_type>/', views.teacher_courses_specific_one_attendance, name='teacher_courses_specific_one_attendance'),
    
    #ADMIN
    path('admin_page/', views.admin_page, name='admin_page'),
]