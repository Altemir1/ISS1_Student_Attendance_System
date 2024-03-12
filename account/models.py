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
    advisor = models.CharField(max_length=255, blank=False)
    major_program = models.CharField(max_length=255, blank=False)
    def __str__(self):
        return f"{self.student_id} {self.fullName}"

class Teacher(CustomUser):
    teacher_id = models.CharField(max_length=20, unique=True, blank=False)
    status = models.CharField(max_length=255, blank=False)
    def __str__(self):
        return f"{self.teacher_id} {self.fullName}"

