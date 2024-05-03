from django.db import models
from django.utils import timezone

class teachers_courses(models.Model):
    teacher_id = models.CharField(max_length=9, blank=False)
    specific_course_id = models.IntegerField(blank=False,default=0)
    class Meta:
        unique_together = ('teacher_id', 'specific_course_id')
    
    def __str__(self):
        return f' {self.teacher_id} - {self.specific_course_id}'

class course(models.Model):
    course_code = models.CharField(max_length=7,unique=True,blank=False)
    credits = models.CharField(max_length=5,blank=False)
    hours = models.IntegerField(blank=False,default=45)
    course_name = models.CharField(max_length=60,blank=False)
    ECTS = models.IntegerField(blank=False,default=5)
    
    def __str__(self):
        return f'{self.course_code} - {self.course_name}'

class students_courses(models.Model):
    student_id = models.CharField(max_length=9, blank=False)
    specific_course_id = models.IntegerField(blank=False,default=0)
    class Meta:
        unique_together = ('student_id', 'specific_course_id')
    
    def __str__(self):
        return f'{self.student_id} - {self.specific_course_id}'

class attendance(models.Model):
    student_id = models.CharField(max_length=9, blank=False)
    specific_course_id = models.IntegerField(blank=False,default=0)
    status=models.IntegerField(blank=False,default=0) # 0 - is P and 1 - is attendant 2 - is absent
    weak_count = models.IntegerField(blank=False,default=0)
    att_id = models.IntegerField(blank=False,unique=True,default=0)
    date = models.DateField(blank=True, null=True)
    
    def __str__(self):
        return f'{self.student_id} - {self.specific_course_id} - week{self.weak_count} - id{self.att_id}'

class specific_course(models.Model):
    course_code = models.CharField(max_length=7,blank=False)
    is_lecture=models.BooleanField(default=True,blank=False)
    specific_course_id = models.IntegerField(blank=False,default=0,unique=True)
    group = models.IntegerField(blank=False,default=0)
    course_part = models.IntegerField(blank=False,default=0)
    course_start_time = models.TimeField()
    course_start_day = models.IntegerField(blank=False,default=0) # monday is 1 , sunday is 7 etc
    registration_deadline = models.DateTimeField(default=timezone.now(), blank=False)
    
    def __str__(self):
        rep = f'{self.course_code} {self.group}-'
        if self.is_lecture:
            rep += 'N'
        else:
            rep += 'P'
        return rep + f' {self.course_start_time}  id{self.specific_course_id}'

class card_of_student(models.Model):
    uid = models.CharField(max_length=8,blank=False)
    student_id = models.CharField(max_length=9, blank=False)
