from django.db import models
from django.contrib.auth.models import AbstractUser
from account.models import Student, Teacher

class Schedule(models.Model):
    schedule_id = models.AutoField(primary_key=True)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    course = models.ForeignKey('Course', on_delete=models.CASCADE)
    classroom = models.ForeignKey('Classroom', on_delete=models.CASCADE)
    day_of_week = models.CharField(max_length=10)
    start_time = models.TimeField()
    end_time = models.TimeField()
    group = models.CharField(max_length=10)
    def __str__(self):
        return f"{self.student.student_id} - {self.course.course_code} - {self.teacher.fullName} - {self.day_of_week} - {self.start_time} - {self.end_time}"

class Course(models.Model):
    course_id = models.AutoField(primary_key=True)
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    credits = models.CharField(max_length=10)
    ects = models.DecimalField(max_digits=2, decimal_places=0)
    course_code = models.CharField(max_length=20)
    course_name = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.course_code} - {self.course_name}"

class Classroom(models.Model):
    classroom_id = models.AutoField(primary_key=True)
    room_number = models.CharField(max_length=20)

    def __str__(self):
        return f"{self.room_number}"

class Attendance(models.Model):
    attendance_id = models.AutoField(primary_key=True)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    schedule = models.ForeignKey(Schedule, on_delete=models.CASCADE)
    entry_time = models.DateTimeField(auto_now_add=True)
    exit_time = models.DateTimeField(null=True, blank=True)
    date = models.DateTimeField(auto_now_add=True)
    present = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.student.student_id} - {self.schedule.course.course_code} - {self.entry_time}"

class Reason(models.Model):
    reason_id = models.AutoField(primary_key=True)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    course = models.ForeignKey('Course', on_delete=models.CASCADE)
    reason = models.TextField()
    document_attached = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.reason}"

class AttendanceStatistics(models.Model):
    statistics_id = models.AutoField(primary_key=True)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    total_hours = models.IntegerField(default=0)
    present_hours = models.IntegerField(default=0)
    absent_hours = models.IntegerField(default=0)
    p_hours = models.IntegerField(default=0)
    def __str__(self):
        return f"{self.student.student_id} - {self.course.course_code} - Total: {self.total_hours}, Present: {self.present_hours}, Absent: {self.absent_hours}"