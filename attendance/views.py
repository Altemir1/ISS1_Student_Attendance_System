from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from attendance.models import course, attendance, specific_course, teachers_courses, students_courses
from django.http import HttpResponse

@login_required
def att_toggle(request, att_id, course_code, group, course_type):
    att_row = attendance.objects.get(att_id=att_id)
    value=att_row.status
    value=(value+1)%3
    att_row.status=value
    att_row.save()
    print(att_row.status)
    return redirect('dashboard:teacher_courses_specific_one_attendance',course_code=course_code,  group=group, course_type=course_type)