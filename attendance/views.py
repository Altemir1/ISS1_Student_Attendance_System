from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from attendance.models import course, attendance, specific_course, teachers_courses, students_courses
from django.http import HttpResponse
from django.utils import timezone
from datetime import timedelta

@login_required
def att_toggle(request, att_id, course_code, group, course_type):
    att_row = attendance.objects.get(att_id=att_id)
    value=att_row.status
    if value == 0 or value == 3: 
        print("No")
    else:    
        value=(value+1)%3
        if value == 0 :
            value=1
    att_row.status=value
    att_row.save()
    print(att_row.status)
    return redirect('dashboard:teacher_courses_specific_one_attendance',course_code=course_code,  group=group, course_type=course_type)

@login_required
def open_registration(request, course_code, group, course_type):
    is_lecture = False
    if course_type == "L":
        is_lecture = True
    
    the_courses = specific_course.objects.filter(course_code=course_code, group=group, is_lecture=is_lecture)
    
    registration_open_until = timezone.now() + timedelta(seconds=60)

    the_courses.update(registration_deadline=registration_open_until)
    
    return redirect('dashboard:teacher_courses_specific_one', course_code=course_code, course_type=course_type)

@login_required
def manual_attendance(request,course_code, is_lecture):
    if is_lecture=="1":
        is_lecture = True
    else:
        is_lecture = False
    
    specific_course_ids_of_a_student = students_courses.objects.filter(student_id=request.user.student.id).values_list('specific_course_id', flat=True)
    needed_ids_for_attendance = specific_course.objects.filter(specific_course_id__in=specific_course_ids_of_a_student, is_lecture=is_lecture,course_code=course_code).values_list('specific_course_id', flat=True)
    
    current_free_id = len(attendance.objects.all())
    
    all_attendances = attendance.objects.filter(specific_course_id__in=needed_ids_for_attendance, student_id=request.user.student.id ).values_list('weak_count', flat=True)
    week_count=0
    if len(all_attendances)==0:
        week_count=1
    else:
        for wc in all_attendances:
            if week_count < wc:
                week_count=wc
        week_count+=1
    for each_id in needed_ids_for_attendance:
        attendance_item = attendance(
            student_id=request.user.student.id,
            specific_course_id=each_id,
            status=3,  # Default status, you can change it as needed
            weak_count=week_count,  # Default weak_count, you can change it as needed
            att_id=current_free_id  # Default att_id, you can change it as needed
        )
        
        attendance_item.save()
        current_free_id+=1
    
    return redirect('dashboard:student_courses_specific_one', course_code=course_code)

def card_reader(uid):
    # Your view logic here
    response_text = f"UID: {uid}"
    
    return HttpResponse(response_text, content_type="text/plain")