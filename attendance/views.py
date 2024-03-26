from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from attendance.models import Course, Schedule, Attendance

@login_required
def student_att(request, course_id, student_id):
    if request.user.is_student:
        course = Course.objects.get(course_id=course_id)
        schedules = Schedule.objects.filter(course=course, student=student_id)
        attendances = Attendance.objects.filter(schedule__in=schedules, student_id=student_id)
        return render(request, 'attendance/student_att.html', {'course': course, 'schedules': schedules, 'attendances': attendances})
    else:
        return redirect('account:login')