from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from attendance.models import course, attendance, specific_course, teachers_courses, students_courses
# Create your views here.

@login_required
def dashboard(request):
    if request.user.is_student:
        
        course_codes = []
        course_info = [] # it will contain array [p, present, absent]
        
        gen_courses_info = []
        
        #Geting into students_courses table 
        specific_course_ids_of_a_student = students_courses.objects.filter(student_id=request.user.student.id).values_list('specific_course_id', flat=True)
        
        for id_specific_course in specific_course_ids_of_a_student:
            
            # inside students_courses table and getting into specific courses table  
            course_of_student = specific_course.objects.filter(specific_course_id=id_specific_course).first()
            
            # checking each specific course for attendance
            if course_of_student.course_code in course_codes:
                for i, existing in enumerate(course_codes):
                    if existing == course_of_student.course_code:
                        
                        present=len(attendance.objects.filter(student_id=request.user.student.id, specific_course_id=id_specific_course,status=1))
                        P=len(attendance.objects.filter(student_id=request.user.student.id,specific_course_id=id_specific_course,status=0))
                        absent=len(attendance.objects.filter(student_id=request.user.student.id,specific_course_id=id_specific_course,status=2))
                        
                        course_info[i][0]=course_info[i][0]+P
                        course_info[i][1]=course_info[i][1]+present
                        course_info[i][2]=course_info[i][2]+absent
                        break
            else:
                course_codes.append(course_of_student.course_code)
                
                present=len(attendance.objects.filter(student_id=request.user.student.id,specific_course_id=id_specific_course,status=1))
                P=len(attendance.objects.filter(student_id=request.user.student.id,specific_course_id=id_specific_course,status=0))
                absent=len(attendance.objects.filter(student_id=request.user.student.id,specific_course_id=id_specific_course,status=2))
                
                course_info.append([P,present,absent])
    
        for i, code in enumerate(course_codes):
            course_obj = course.objects.filter(course_code=code).first()
            gen_courses_info.append({
                "course_code":code,
                "course_name":course_obj.course_name,
                "credits":course_obj.credits,
                "ECTS":course_obj.ECTS,
                "hours":course_obj.hours,
                "present": course_info[i][1],
                "absent": course_info[i][2],
                "P":course_info[i][0],
                "absens_persentage": (course_info[i][2]/course_obj.hours)
            })
        
        return render(request, 'dashboard/gen_attendance_info.html', {'student_courses': gen_courses_info})

    elif request.user.is_teacher:
        teacher_courses = []
        course_codes = []
        specific_course_ids_of_a_teacher = teachers_courses.objects.filter(teacher_id=request.user.teacher.id).values_list('specific_course_id', flat=True)
        
        for c_id in specific_course_ids_of_a_teacher:
            courses_of_teacher = specific_course.objects.filter(specific_course_id=c_id)
            for c in courses_of_teacher:
                course_codes.append(c.course_code)
        
        course_codes=list(set(course_codes))
        
        for code in course_codes:
            course_obj = course.objects.filter(course_code=code).first()
            teacher_courses.append(course_obj)
        
        return render(request, 'dashboard/gen_courses_info.html', {'teacher_courses': teacher_courses})

    else:
        return redirect('account:login')
'''
@login_required
def specific_course_t(request, course_id, teacher_id):
    if request.user.is_teacher:
        course = Course.objects.get(course_id=course_id)
        schedules = Schedule.objects.filter(course=course, teacher=teacher_id)
        return render(request, 'dashboard/course_dashboard.html', {'course': course, 'schedules': schedules})
    else:
        return redirect('account:login')
'''
@login_required
def specific_course(request, course_code, id):
    if request.user.is_student:
        course = Course.objects.get(course_id=course_id)
        schedules = Schedule.objects.filter(course=course, student=student_id)
        attendances = Attendance.objects.filter(schedule__in=schedules, student_id=student_id)
        
        return render(request, 'dashboard/specific_course_attendance.html', {'course': course, 'schedules': schedules, 'attendances': attendances})
    elif request.user.is_teacher:
        pass
    else:
        return redirect('account:login')

def certificate_submission(request):
    if request.user.is_student:
        #Kanat please help ;)
        return render(request, 'dashboard/notice_document_submission.html')
    else:
        return redirect('account:login')
