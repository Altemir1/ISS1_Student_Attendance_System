from django.test import TestCase, Client
from django.urls import reverse
from attendance.models import attendance, specific_course, students_courses, course, teachers_courses
from dashboard.views import student_profile
from account.models import CustomUser, Student, Teacher
from datetime import time
from django.core.files.uploadedfile import SimpleUploadedFile
from dashboard.forms import DocumentSubmissionForm

class StudentProfileTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = Student.objects.create_user(
            id='testuser', password='testpassword')
        self.client.login(username=self.user.id, password='testpassword')

    def test_student_profile_view(self):
        response = self.client.get(reverse('dashboard:student_profile'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'dashboard/profile_student.html')

class StudentCoursesTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = Student.objects.create_user(
            id='testuser', password='testpassword')
        self.client.login(username=self.user.id, password='testpassword')

    def test_student_courses_view(self):
        response = self.client.get(reverse('dashboard:student_courses'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'dashboard/courses_student.html')



class StudentCoursesSpecificOneTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = Student.objects.create_user(
            id='testuser', password='testpassword')
        self.client.login(username=self.user.id, password='testpassword')
        self.teacher = Teacher.objects.create_user(
            id='testteach', password='testpassword' , email='teach@sdu.kz'
        )
        self.course_code = 'CS101'
        self.specific_course = specific_course.objects.create(
            course_code=self.course_code,
            is_lecture = True,
            specific_course_id = 1,
            group = 3,
            course_part = 0,
            course_start_time = time(8, 30, 0),
            course_start_day = 0
        )
        self.student_courses = students_courses.objects.create(
            student_id = 'testuser',
            specific_course_id = 1
        )
        self.course = course.objects.create(
            course_code = 'CS101',
            credits = '5',
            hours = 45,
            course_name = 'Software Engineering',
            ECTS = 5,
        )
        self.teacher_courses = teachers_courses.objects.create(
            teacher_id = 'testteach',
            specific_course_id = 1
        )

    def test_student_courses_specific_one_view(self):
        response = self.client.get(reverse('dashboard:student_courses_specific_one', args=(self.course_code,)))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'dashboard/course_specific_student.html')

class TeacherViewsTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.teacher = Teacher.objects.create_user(
            id='testteach', password='testpassword'
        )
        self.course1 = course.objects.create(
            course_code='CS101',
            credits='3',
            hours=45,
            course_name='Introduction to Computer Science',
            ECTS=5
        )

        self.course2 = course.objects.create(
            course_code='MATH101',
            credits='3',
            hours=45,
            course_name='Calculus I',
            ECTS=5
        )

        self.specific_course1 = specific_course.objects.create(
            course_code='CS101',
            is_lecture=True,
            specific_course_id=1,
            course_part=1,
            course_start_time=time(8, 30, 0),
            course_start_day=1
        )

        self.specific_course2 = specific_course.objects.create(
            course_code='CS101',
            is_lecture=False,
            specific_course_id=2,
            course_part=2,
            course_start_time=time(10, 30, 0),
            course_start_day=1
        )

        self.specific_course3 = specific_course.objects.create(
            course_code='MATH101',
            is_lecture=True,
            specific_course_id=3,
            course_part=1,
            course_start_time=time(13, 30, 0),
            course_start_day=1
        )

        teachers_courses.objects.create(
            teacher_id='testteach',
            specific_course_id=1
        )

        teachers_courses.objects.create(
            teacher_id='testteach',
            specific_course_id=2
        )

        teachers_courses.objects.create(
            teacher_id='testteach',
            specific_course_id=3
        )

        self.client.post(reverse('account:login'), {'id': 'testteach', 'password': 'testpassword', 'role':'teacher'})

    def test_teacher_profile(self):
        response = self.client.get(reverse('dashboard:teacher_profile'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'dashboard/profile_teacher.html')

    def test_teacher_courses(self):
        response = self.client.get(reverse('dashboard:teacher_courses'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'dashboard/courses_teacher.html')


class DashboardViewsTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.student = Student.objects.create_user(
            id='testid', password='testpassword'
        )
        self.client.post(reverse('account:login'), {'id': 'testid', 'password': 'testpassword', 'role':'student'})

    def test_student_document_submission(self):
        mock_file = SimpleUploadedFile('test.pdf', b'file_content', content_type='application/pdf')
        mock_form = DocumentSubmissionForm(data={'description': 'Test description'}, files={'document': mock_file})

        response = self.client.post(reverse('dashboard:student_document_submission'), data=mock_form.data, files=mock_form.files)

        self.assertEqual(response.status_code, 200)
