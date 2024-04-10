from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Student, Teacher, CustomUser
from .forms import TeacherCreationForm, StudentCreationForm
# Register your models here.

admin.site.register(CustomUser, UserAdmin)

class CustomTeacherAdmin(UserAdmin):
    add_form = TeacherCreationForm
    model = Teacher

admin.site.register(Teacher, CustomTeacherAdmin)

class CustomStudentAdmin(UserAdmin):
    add_form = StudentCreationForm
    model = Student
    list_display = ('id', 'email', 'advisor', 'major_program')

admin.site.register(Student, CustomStudentAdmin)