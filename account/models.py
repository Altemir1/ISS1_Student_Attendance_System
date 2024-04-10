from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    email = models.EmailField(max_length=255, blank=False, unique=True)
    id = models.CharField(max_length=20, unique=True, blank=False, primary_key=True)
    USERNAME_FIELD = 'id'
    @property
    def is_student(self):
        return hasattr(self, 'student')
    @property
    def is_teacher(self):
        return hasattr(self, 'teacher')

class Student(CustomUser):
    advisor = models.CharField(max_length=255, blank=False)
    major_program = models.CharField(max_length=255, blank=False)
    def __str__(self):
        return f"{self.student_id} {self.first_name}"

class Teacher(CustomUser):
    status = models.CharField(max_length=255, blank=False)
    def __str__(self):
        return f"{self.teacher_id} {self.first_name}"


