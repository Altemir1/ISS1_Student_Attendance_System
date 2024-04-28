from django.contrib import admin
from .models import teachers_courses, course, students_courses, attendance, specific_course, card_of_student

admin.site.register(teachers_courses)
admin.site.register(course)
admin.site.register(students_courses)
admin.site.register(attendance)
admin.site.register(specific_course)
admin.site.register(card_of_student)