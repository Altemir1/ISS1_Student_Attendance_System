from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from attendance.models import Course
# Create your views here.

@login_required
def dashboard(request):
    if request.user.is_student:
        student_courses = Course.objects.filter(schedule__student=request.user.student)
        return render(request, 'dashboard/gen_attendance_info.html', {'student_courses': student_courses})
    elif request.user.is_teacher:    
        teacher_courses = Course.objects.filter(teacher=request.user.teacher)
        return render(request, 'dashboard/teacher_dashboard.html', {'teacher_courses': teacher_courses})