from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from attendance.models import course, attendance, specific_course, teachers_courses, students_courses
from account.models import Teacher
import math

@login_required
def student_profile(request):
    return render(request, 'dashboard/profile_student.html',{'status1':"active",'status2':"",'status3':""})
    
@login_required
def student_courses(request):
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
            "absens_persentage": math.ceil(course_info[i][2]/course_obj.hours)
        })
    
    return render(request, 'dashboard/courses_student.html', {'student_courses': gen_courses_info, 'status1':"",'status2':"active",'status3':""})

@login_required
def student_courses_specific_one(request,  course_code=None):
    specific_course_ids_of_a_student = students_courses.objects.filter(student_id=request.user.student.id).values_list('specific_course_id', flat=True)
    course_obj = course.objects.filter(course_code=course_code).first()
    course_item = {}
    
    course_item['course_code']=course_obj.course_code
    course_item['course_name']=course_obj.course_name
    
    course_code_matched_ids_l = []
    course_code_matched_ids_p = []
    
    practice_groupe = None
    lecture_groupe = None
    
    for specific_course_id in specific_course_ids_of_a_student:
        course_of_student = specific_course.objects.filter(specific_course_id=specific_course_id).first()
        if course_of_student.course_code==course_code:
            if course_of_student.is_lecture==False:
                course_code_matched_ids_p.append(specific_course_id)
                practice_groupe=course_of_student.group
            else :
                course_code_matched_ids_l.append(specific_course_id)
                lecture_groupe=course_of_student.group
    
    course_item['groupe']={'practice':practice_groupe,'lecture':lecture_groupe}
    
    lecturer_id =teachers_courses.objects.filter(specific_course_id=course_code_matched_ids_l[0]).first().teacher_id
    lecturer = Teacher.objects.filter(id=lecturer_id).first()
    
    course_item['lecturer']=lecturer.first_name+" "+lecturer.last_name
    course_item['lecturer_status']=lecturer.status
    
    lecture_attendances = []
    attendances = attendance.objects.filter(student_id=request.user.student.id,specific_course_id__in=course_code_matched_ids_l)
    
    for att in attendances:
        start_time= specific_course.objects.filter(specific_course_id=att.specific_course_id).first().course_start_time
        lecture_attendances.append({
            "week":str(att.weak_count)+"W",
            "status":att.status,
            "start_time":start_time
        })
    
    if len(course_code_matched_ids_p)==0:
        return render(request, 'dashboard/course_specific_student.html', {'course': course_item,'lecture_attendances':lecture_attendances,})
    else :
        practice_attendances = []
        attendances = attendance.objects.filter(student_id=request.user.student.id,specific_course_id__in=course_code_matched_ids_p)

        practice_teacher_id =teachers_courses.objects.filter(specific_course_id=course_code_matched_ids_l[0]).first().teacher_id
        practice_teacher = Teacher.objects.filter(id=practice_teacher_id).first()
        
        course_item['practice_teacher']=practice_teacher.first_name+" "+practice_teacher.last_name
        course_item['practice_teacher_status']=practice_teacher.status

        for att in attendances:
            start_time= specific_course.objects.filter(specific_course_id=att.specific_course_id).first().course_start_time
            practice_attendances.append({
                "week":str(att.weak_count)+"W",
                "status":att.status,
                "start_time":start_time
            })
        return render(request, 'dashboard/course_specific_student.html', {'course': course_item,'lecture_attendances':lecture_attendances,'practice_attendances':practice_attendances,})


@login_required
def teacher_courses(request):
    teacher_courses = []
    specific_course_ids_of_a_teacher = teachers_courses.objects.filter(teacher_id=request.user.teacher.id).values_list('specific_course_id', flat=True)
    courses_of_a_teacher = specific_course.objects.filter(specific_course_id__in = specific_course_ids_of_a_teacher)
    map_of_courses = [] 
    
    for crs in courses_of_a_teacher:
        course_name=course.objects.filter(course_code=crs.course_code).first().course_name
        type_of_course = "P"
        if crs.is_lecture==True:
            type_of_course="L"
        
        if course_name+type_of_course not in map_of_courses:
            map_of_courses.append(course_name+type_of_course)
            teacher_courses.append({
                "course_code":crs.course_code,
                "course_name":course_name,
                "course_type":type_of_course,
            })
    
    return render(request, 'dashboard/gen_courses_info.html', {'teacher_courses': teacher_courses})

@login_required
def teacher_course_displayer(request, course_code=None, course_type=None):
    return render(request, 'dashboard/choosing_current_cource.html', {'course': None})

def student_document_submission(request):
    return
# #Gotta fix this 
# @login_required
# def student_document_submission(request):
#     if request.method == 'POST':
        
#         form = HealthIssueForm(request.POST, request.FILES)
        
#         if form.is_valid():
#             title = form.cleaned_data['title']
#             description = form.cleaned_data['description']
#             document = form.cleaned_data['document']
            
#             # Save the form data to the database
#             health_issue = HealthIssue(title=title, description=description, document=document)
#             health_issue.save()
            
#             messages.success(request, 'Health issue document submitted successfully.')
#             return redirect('submit_health_issue')  # Redirect to the same page or another page
            
#         else:
#             messages.error(request, 'Error submitting the health issue document. Please check the form.')
            
#     else:
#         form = HealthIssueForm()
    
#     context = {
#         'form': form
#     }
    
#     return render(request, 'health_issue_form.html', context)
