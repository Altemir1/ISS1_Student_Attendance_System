from django.contrib import admin
from .models import Schedule, Course, Classroom, Attendance, Reason, AttendanceStatistics

admin.site.register(Schedule)
admin.site.register(Course)
admin.site.register(Classroom)
admin.site.register(Attendance)
admin.site.register(Reason)
admin.site.register(AttendanceStatistics)