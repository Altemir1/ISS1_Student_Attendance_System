ISS1_Student_Attendance_System
This repository was created for academical project for "Software Engineering" classes. Code: CSS 342.

To add Users through console PS. please replace the info kindly Yerzhan

python manage.py shell
from account.models import Student  
student = Student.objects.create(id='210107078', email='210107078@stu.sdu.edu.kz', first_name='Yerzhan', last_name='Sultanov', advisor='Gulnara Saymasay', major_program='Computer Science')
student.set_password("admin")
student.save()