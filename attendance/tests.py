from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from attendance.models import Course, Schedule, Attendance, Classroom
from account.models import Student, Teacher

class StudentAttViewTests(TestCase):

    def setUp(self):
        self.student = Student.objects.create_user(
            username='studentuser',
            password='testpassword',
            email='test2@example.com',
            fullName='Test User',
            student_id='2'
        )
        
        self.teacher = Teacher.objects.create_user(
            username='teacheruser',
            password='teacherpassword',
            email='test1@example.com',
            fullName='Test User',
            teacher_id='1'
        )
        
        self.course = Course.objects.create(
            course_code='COMP101',
            course_name='Introduction to Computer Science',
            credits='3',
            ects='6',
            teacher=self.teacher
        )
        
        # Create a classroom
        self.classroom = Classroom.objects.create(
            room_number='D114'
        )
        
        self.schedule = Schedule.objects.create(
            student=self.student,
            course=self.course,
            teacher=self.teacher,
            day_of_week='Monday',
            start_time='08:00:00',
            end_time='09:00:00',
            classroom = self.classroom,
            group = '01_N'
        )
        # Create an attendance
        self.attendance = Attendance.objects.create(
            schedule=self.schedule,
            student = self.student,
            entry_time='2024-03-27 08:00:00',  
            exit_time='2024-03-27 09:00:00',
            date='2024-03-27 00:00:00',
            present = True
        )
    def test_student_att_view(self):

        # Log in the student
        self.client.login(username='studentuser', password='testpassword')

        # Make a request to the student_att view with the necessary arguments
        response = self.client.get(reverse('attendance:student_att', args=[self.course.course_id, self.student.id]))

        # Check that the response is 200 OK
        self.assertEqual(response.status_code, 200)

        # Check that the course is displayed
        self.assertContains(response, 'COMP101')

        # Check that the schedule is displayed
        # Check that the attendance is displayed
        self.assertContains(response, '✅')
        self.assertContains(response, self.student.fullName)
        # Log out the student
        self.client.logout()

        # Check that the student is redirected to the login page
        response = self.client.get(reverse('attendance:student_att', args=[self.course.course_id, self.student.id]))
        self.assertEqual(response.status_code, 302)