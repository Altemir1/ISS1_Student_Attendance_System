from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from attendance.models import attendance, specific_course, course
from attendance.views import att_toggle
from account.models import  Teacher, Student
from datetime import time
class AttendanceViewsTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.student = Student.objects.create_user(
            id='testid', password='testpassword', email='testemail@sdu.kz'
        )
        self.teacher = Teacher.objects.create_user(
            id='testteach', password='testpassword'
        )
        self.course = course.objects.create(
            course_code='CS101',
            credits='3',
            hours=45,
            course_name='Introduction to Computer Science',
            ECTS=5
        )
        self.specific_course = specific_course.objects.create(
            course_code='CS101',
            is_lecture=True,
            specific_course_id=1,
            course_part=1,
            course_start_time=time(8, 30, 0),
            course_start_day=1
        )
        self.attendance = attendance.objects.create(
            student_id='testid',
            specific_course_id=1,
            status=0,
            weak_count = 1,
            att_id = 1,
        )
        self.client.post(reverse('account:login'), {'id': 'testteach', 'password': 'testpassword', 'role':'teacher'})

    def test_att_toggle(self):
        response = self.client.get(reverse('attendance:att_toggle', args=('1', 'CS101', '1', 'L')))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(attendance.objects.get(att_id='1').status, 1)