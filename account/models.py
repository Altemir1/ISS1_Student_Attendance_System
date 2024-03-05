from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    fullName = models.CharField(max_length=255, blank=False)
    email = models.EmailField(max_length=255, blank=False, unique=True)

    @property
    def is_student(self):
        return hasattr(self, 'student')

    @property
    def is_teacher(self):
        return hasattr(self, 'teacher')

class Student(CustomUser):
    student_id = models.CharField(max_length=20, unique=True, blank=False)
    def __str__(self):
        return f"{self.student_id} {self.fullName}"

class Teacher(CustomUser):
    teacher_id = models.CharField(max_length=20, unique=True, blank=False)
    def __str__(self):
        return f"{self.teacher_id} {self.fullName}"


class Course(models.Model):
    name = models.CharField(max_length=100)
    course_id = models.CharField(max_length=12,unique=True,blank=False) # ex : 'css427-1-l-1' or 'css427-2-p-1' (id)-(groupe)-(practice or lecture)-(hour)
    start_time = models.DateField()
    def __str__(self):
        return f"{self.course_id} {self.name}"

class Attendance(models.Model):
    course_id = models.CharField(max_length=12,unique=True,blank=False) # ex : 'css427-l-1' or 'css427-p-1'
    entity_id = models.CharField(max_length=20, unique=True, blank=False) # Whoever this is Teacher or Student
    registration_date = models.DateField(auto_now_add=True)  # Date of attendance
    registration_time = models.TimeField(auto_now_add=True)  # Time of attendance
    really_attended = models.BooleanField(blank=False)
    def __str__(self):
        return  f"{self.registration_date} {self.registration_time} {self.course_id} {self.entity_id}"

class CourseInstructor(models.Model):
    course_id = models.CharField(max_length=12,unique=True,blank=False)
    teacher_id = models.CharField(max_length=20, unique=True, blank=False)
    def __str__(self):
        return f"Course id: {self.course_id}, Teachers id: {self.teacher_id}"

class StudentsCourses(models.Model):
    course_id = models.CharField(max_length=12,unique=True,blank=False)
    student_id = models.CharField(max_length=20, unique=True, blank=False)
    def __str__(self):
        return f"Course id: {self.course_id}, Students id: {self.teacher_id}"

# Excuse_ table