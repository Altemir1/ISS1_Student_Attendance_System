from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from attendance.models import Course, Schedule, Attendance, AttendanceStatistics
# Create your views here.

@login_required
def dashboard(request):
    if request.user.is_student:
        student_courses = Schedule.objects.filter(student=request.user.student).values_list('course__course_code', flat=True).distinct()
        student_courses = Course.objects.filter(course_code__in=student_courses)

        for course in student_courses:
            stat = AttendanceStatistics.objects.filter(student=request.user.student, course=course).first()
            course.attendance_stats = {
                'total_hours': stat.total_hours,
                'present_hours': stat.present_hours,
                'absent_hours': stat.absent_hours,
                'p_hours': stat.p_hours,
            }

        return render(request, 'dashboard/gen_attendance_info.html', {'student_courses': student_courses})

    elif request.user.is_teacher:
        teacher_courses = Course.objects.filter(teacher=request.user.teacher)
        return render(request, 'dashboard/teacher_dashboard.html', {'teacher_courses': teacher_courses})

    else:
        return redirect('account:login')

@login_required
def course_dashboard(request, course_id, teacher_id):
    if request.user.is_teacher:
        course = Course.objects.get(course_id=course_id)
        schedules = Schedule.objects.filter(course=course, teacher=teacher_id)
        return render(request, 'dashboard/course_dashboard.html', {'course': course, 'schedules': schedules})
    else:
        return redirect('account:login')
