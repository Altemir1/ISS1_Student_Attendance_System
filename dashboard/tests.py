from django.test import RequestFactory
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import TestCase
from account.models import Student, Teacher
from attendance.models import Course, AttendanceStatistics, Schedule, Classroom

class DashboardViewTests(TestCase):

    def setUp(self):
        # Create a user
        self.teacher = Teacher.objects.create_user(
            username='teacheruser',
            password='teacherpassword',
            email='test1@example.com',
            fullName='Test User',
            teacher_id='1'
        )
        self.student = Student.objects.create_user(
            username='studentuser',
            password='testpassword',
            email='test2@example.com',
            fullName='Test User',
            student_id='2'
        )

        # Create a course
        self.course = Course.objects.create(
            course_code='COMP101',
            course_name='Introduction to Computer Science',
            credits='3',
            ects='6',
            teacher=self.teacher
        )
        
        self.classroom = Classroom.objects.create(
            room_number='D114'
        )
        # Create a schedule
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

        # Create attendance statistics for the course
        self.at = AttendanceStatistics.objects.create(
            student=self.student,
            course=self.course,
            total_hours=50,
            present_hours=40,
            absent_hours=10,
            p_hours=2
        )
    def test_dashboard_view_by_student(self):
        # Log in the user
        self.client.login(username='studentuser', password='testpassword')

        # Get the dashboard view
        response = self.client.get(reverse('dashboard:dashboard'))

        # Check that the response is 200 OK
        self.assertEqual(response.status_code, 200)

        # Check that the course is displayed
        self.assertContains(response, 'COMP101')
        self.assertContains(response, '50')
        self.assertContains(response, str(int(round((self.at.absent_hours/self.at.total_hours)*100))))
        # Log out the user
        self.client.logout()

        # Check that the user is redirected to the login page
        response = self.client.get(reverse('dashboard:dashboard'))
        self.assertEqual(response.status_code, 302)

    def test_dashboard_view_by_teacher(self):

        # Log in the teacher
        self.client.login(username='teacheruser', password='teacherpassword')

        # Get the dashboard view
        response = self.client.get(reverse('dashboard:dashboard'))

        # Check that the response is 200 OK
        self.assertEqual(response.status_code, 200)

        # Check that the course is displayed
        self.assertContains(response, 'COMP101')

        # Log out the teacher
        self.client.logout()

        # Check that the teacher is redirected to the login page
        response = self.client.get(reverse('dashboard:dashboard'))
        self.assertEqual(response.status_code, 302)

class CourseDashboardViewTests(TestCase):

    def setUp(self):
        # Create a teacher
        self.teacher = Teacher.objects.create_user(
            username='teacheruser',
            password='teacherpassword',
            email='test1@example.com',
            fullName='Test User',
            teacher_id='1'
        )

        # Create a course
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

        self.student = Student.objects.create_user(
            username='studentuser',
            password='testpassword',
            email='test2@example.com',
            fullName='Test User',
            student_id='2'
        )
        # Create a schedule
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

    def test_course_dashboard_view(self):

        # Log in the teacher
        self.client.login(username='teacheruser', password='teacherpassword')

        # Get the course dashboard view
        response = self.client.get(reverse('dashboard:course_dashboard', args=[self.course.course_id, self.teacher.teacher_id]))

        # Check that the response is 200 OK
        self.assertEqual(response.status_code, 200)
        # Check that the course is displayed
        self.assertContains(response, 'Introduction to Computer Science')
        self.assertContains(response, '01_N')
        # Check that the schedule is displayed
        self.assertContains(response, 'D114')

        # Log out the teacher
        self.client.logout()

        # Check that the teacher is redirected to the login page
        response = self.client.get(reverse('dashboard:course_dashboard', args=[self.course.course_id, self.teacher.teacher_id]))
        self.assertEqual(response.status_code, 302)