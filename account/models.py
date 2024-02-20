
from django.db import models

class Student(models.Model):
    student_id = models.CharField(max_length=20, unique=True, blank=False)
    fullName = models.CharField(max_length=255, blank=False),
    password = models.CharField(max_length=255, blank=False),
    email = models.EmailField(max_length=50, blank=False, unique=True)
    
    def __str__(self) -> str:
        return self.student_id + ' ' + self.fullName
    
class Teacher(models.Model):
    teacher_id = models.CharField(max_length=20, unique=True, blank=False)
    fullName = models.CharField(max_length=255, blank=False),
    password = models.CharField(max_length=255, blank=False),
    email = models.EmailField(max_length=50, blank=False, unique=True)
    
    def __str__(self) -> str:
        return self.student_id + ' ' + self.fullName
