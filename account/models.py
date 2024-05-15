from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin

class CustomUserManager(BaseUserManager):
    def create_user(self, id, password=None, **extra_fields):
        if not id:
            raise ValueError("The ID field must be set")
        user = self.model(id=id, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, id, password=None, **extra_fields):
        extra_fields.setdefault('is_superuser', True)
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        return self.create_user(id, password, **extra_fields)

class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(max_length=255, blank=False, unique=True)
    id = models.CharField(max_length=9, unique=True, blank=False, primary_key=True)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    objects = CustomUserManager()
    
    USERNAME_FIELD = 'id'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    def __str__(self):
        return self.email

    def get_full_name(self):
        return f"{self.first_name} {self.last_name}"

    def get_short_name(self):
        return self.first_name

    @property
    def is_student(self):
        return hasattr(self, 'student')

    @property
    def is_teacher(self):
        return hasattr(self, 'teacher')
    @property
    def is_staff(self):
        return self.is_superuser
    @property
    def is_admin(self):
        return hasattr(self, 'admin')
    
class Student(CustomUser):
    advisor = models.CharField(max_length=255, blank=False)
    major_program = models.CharField(max_length=255, blank=False)
    
    def __str__(self):
        return f"{self.id} {self.first_name}"  # Changed from student_id to id

class Teacher(CustomUser):
    status = models.CharField(max_length=255, blank=False)
    
    def __str__(self):
        return f"{self.id} {self.first_name}"  # Changed from teacher_id to id

class Admin(CustomUser):
    
    def __str__(self):
        return f"{self.id} {self.first_name}"  