from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from attendance.models import course, attendance, specific_course, teachers_courses, students_courses, card_of_student
from django.http import HttpResponse
from django.utils import timezone
from datetime import timedelta, datetime
from account.models import Teacher, Student

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
    current_date = timezone.localtime(timezone.now(), timezone=timezone.get_fixed_timezone(300)).date()
    
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
        
        if not attendance.objects.filter(student_id=request.user.student.id,specific_course_id=each_id,date=current_date).exists():
            attendance_item = attendance(
                student_id=request.user.student.id,
                specific_course_id=each_id,
                status=3,  # Default status, you can change it as needed
                weak_count=week_count,  # Default weak_count, you can change it as needed
                att_id=current_free_id,  # Default att_id, you can change it as needed
                date=current_date
            )

            attendance_item.save()
            current_free_id+=1

    return redirect('dashboard:student_courses_specific_one', course_code=course_code)

def card_reader(request):
    uid = request.GET.get('uid', '')

    # Check if a UID is provided
    if uid:
        # Your logic here
        current_date_time = timezone.localtime(timezone.now(), timezone=timezone.get_fixed_timezone(300))
        
        current_day = (current_date_time.date().weekday()+1)%8
        
        rounded_minutes = (current_date_time.minute // 15 + 1) * 15
        rounded_date = current_date_time.replace(minute=rounded_minutes, second=0, microsecond=0)
        rounded_time = rounded_date.strftime('%H:%M')
        uid=uid[0:len(uid)-1]
        
        id_of_a_student = card_of_student.objects.filter(uid=uid).first()
        
        specific_course_ids_of_a_student = students_courses.objects.filter(student_id=id_of_a_student.student_id).values_list('specific_course_id', flat=True)
        
        posible_attending_courses = specific_course.objects.filter(course_start_day=2,specific_course_id__in=specific_course_ids_of_a_student,course_start_time=rounded_time)
        
        print("id :",id_of_a_student.student_id)
        print("courses of",id_of_a_student.student_id)
        print("current_day",current_day)
        print("rounded_time",rounded_time)
        #if there is a course 
        for crs in posible_attending_courses:
            all_attendances=attendance.objects.filter(specific_course_id=crs.specific_course_id, student_id=id_of_a_student.student_id ).values_list('weak_count', flat=True)
            week_count=1
            for wc in all_attendances:
                if week_count < wc:
                    week_count=wc
            week_count+=1
            attendance_id = len(all_attendances)
            print("The course",crs.course_code)
            
            #SAVE ONLY IF IT DOES NOT ALREADY EXISTS
            if not attendance.objects.filter(student_id=id_of_a_student.student_id,specific_course_id=crs.specific_course_id,date=rounded_date.date()).exists():    
                attendance_item = attendance(
                    student_id=id_of_a_student.student_id,
                    specific_course_id=crs.specific_course_id,
                    status=1, 
                    weak_count=week_count,  # Default weak_count, you can change it as needed
                    att_id=attendance_id,  # Default att_id, you can change it as needed
                    date=rounded_date.date()
                )
                attendance_item.save()

        response_text = f"It worked "

        response_status = 200  # HTTP status code 200 OK
    else:
        response_text = "No UID provided"
        response_status = 400  # HTTP status code 400 Bad Request

    # Return an HTTP response with the response text
    return HttpResponse(response_text, content_type="text/plain", status=response_status)