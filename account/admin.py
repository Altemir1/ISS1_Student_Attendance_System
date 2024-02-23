from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Student, Teacher, CustomUser
# Register your models here.

admin.site.register(CustomUser, UserAdmin)
admin.site.register(Student)
admin.site.register(Teacher)