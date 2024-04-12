from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Student, Teacher, CustomUser
from .forms import TeacherCreationForm, StudentCreationForm
# Register your models here.

class CustomUserAdmin(UserAdmin):
    list_display = ('id', 'first_name', 'last_name', 'email')
    list_filter = ()
    fieldsets = (
        (None, {'fields': ('id', 'email')}),
        ('Personal Info', {'fields': ('first_name', 'last_name')}),
        ('Permissions', {'fields': ('is_active', 'is_superuser')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('id', 'email','password1', 'password2'),
        }),
    )
    search_fields = ('id', 'first_name', 'last_name', 'email')
    ordering = ('id',)

class CustomUserStudent(UserAdmin):
    list_display = ('id', 'first_name', 'last_name', 'email')
    list_filter = ()
    fieldsets = (
        (None, {'fields': ('id', 'email')}),
        ('Personal Info', {'fields': ('first_name', 'last_name')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('id', 'email','advisor','major_program', 'password1', 'password2'),
        }),
    )
    search_fields = ('id', 'first_name', 'last_name', 'email')
    ordering = ('id',)

class CustomUserTeacher(UserAdmin):
    list_display = ('id', 'first_name', 'last_name', 'email')
    list_filter = ()
    fieldsets = (
        (None, {'fields': ('id', 'email')}),
        ('Personal Info', {'fields': ('first_name', 'last_name')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('id', 'email','status', 'password1', 'password2'),
        }),
    )
    search_fields = ('id', 'first_name', 'last_name', 'email')
    ordering = ('id',)


admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Teacher, CustomUserTeacher)
admin.site.register(Student, CustomUserStudent)