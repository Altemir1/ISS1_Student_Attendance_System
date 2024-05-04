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
    return redirect('dashboard:teacher_courses_specific_one_attendance',course_code=course_code,  group=group, course_type=course_type)

@login_required
def open_registration(request, course_code, group, course_type):
    is_lecture = False
    if course_type == "L":
        is_lecture = True

    the_courses = specific_course.objects.filter(course_code=course_code, group=group, is_lecture=is_lecture)

    registration_open_until = timezone.now() + timedelta(seconds=59)

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
    
    attendance_that_will_change = attendance.objects.filter(specific_course_id__in=needed_ids_for_attendance, student_id=request.user.student.id, date = current_date ).first()
    
    if attendance_that_will_change is not None:
    
        attendance_that_will_change.status=3
        
        attendance_that_will_change.save()
    
    return redirect('dashboard:student_courses_specific_one', course_code=course_code)

#card_reader logic 
def card_reader(request):
    uid = request.GET.get('uid', '')

    if uid:
        current_date_time = timezone.localtime(timezone.now(), timezone=timezone.get_fixed_timezone(300))
        
        current_date = current_date_time.date()
        
        if current_date_time.minute<=15:
            rounded_date = current_date_time.replace(minute=0, second=0, microsecond=0)
        else:
            rounded_date = current_date_time.replace(minute=15, second=0, microsecond=0)
                
        rounded_time = rounded_date.strftime('%H:%M')
        
        uid=uid[0:len(uid)-1]
        id_of_a_student = card_of_student.objects.filter(uid=uid).first()
        
        if id_of_a_student is not None:
            specific_course_ids_of_a_student = students_courses.objects.filter(student_id=id_of_a_student.student_id).values_list('specific_course_id', flat=True)
            posible_attending_courses = specific_course.objects.filter(specific_course_id__in=specific_course_ids_of_a_student,course_start_time=rounded_time)
            for crs in posible_attending_courses:
                attendance_that_will_change=attendance.objects.filter(specific_course_id=crs.specific_course_id, student_id=id_of_a_student.student_id, date=current_date).first()
                
                if attendance_that_will_change is not None:
                    print("SHIT HERE WE GO AGAIN")
                    attendance_that_will_change.status=1
                    attendance_that_will_change.save()

        response_text = "It worked "
        response_status = 200  # HTTP status code 200 OK
    else:
        response_text = "No UID provided"
        response_status = 400  # HTTP status code 400 Bad Request

    # Return an HTTP response with the response text
    return HttpResponse(response_text, content_type="text/plain", status=response_status)

def reset_everything(request):
    students = Student.objects.all()
    #WHEN DO ALL THE LESSONS START THE LAST WEEKEND DATE
    naive_datetime = datetime(2024, 2, 11)
    # Make it timezone-aware in UTC
    when_it_all_started = timezone.make_aware(naive_datetime)

    # Convert it to the desired timezone (UTC+5:00)
    when_it_all_started = when_it_all_started.astimezone(timezone.get_fixed_timezone(300))

    
    starting_id_for_attendance = 0
    
    for student in students:
        students_all_courses = students_courses.objects.filter(student_id = student.id)
        for students_cours in students_all_courses:
            cours_start_date = specific_course.objects.filter(specific_course_id=students_cours.specific_course_id).first().course_start_day
            cours_start_date = when_it_all_started+timedelta(days=cours_start_date)
            for i in range(15):
                # Create an instance of the Attendance model
                attendance_instance = attendance.objects.create(
                    student_id=student.id,                                                         # Example student ID
                    specific_course_id=students_cours.specific_course_id,                          # Example course ID
                    status=2,                                                                      # Example status code (0 for P)
                    weak_count=i+1,                                                                # Example week count
                    att_id=starting_id_for_attendance,                                             # Example attendance ID
                    date=cours_start_date+timedelta(days=7*i)                                      # Example date (in YYYY-MM-DD format)
                )
                # Save the instance
                attendance_instance.save()
                starting_id_for_attendance+=1
    return HttpResponse("HEY ALL THE ATTENDANCES HAVE BEEN SET", content_type="text/plain", status=200)