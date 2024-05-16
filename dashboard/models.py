from django.db import models
from account.models import CustomUser
from attendance.models import attendance
# Create your models here.

class SubmittedDocument(models.Model):
    student = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="documents")
    description = models.TextField()
    document = models.FileField(upload_to='student_documents/')
    submitted_at = models.DateTimeField(auto_now_add=True)
    from_date = models.DateTimeField(blank=False)
    to_date = models.DateTimeField(blank=False)
    ACCEPTED_CHOICES = [
        (0, 'Not Checked'),
        (1, 'Accepted'),
        (2, 'Rejected')
    ]
    accepted = models.IntegerField(default=0, choices=ACCEPTED_CHOICES)
    def __str__(self):
        return f"{self.student.id} -  {self.document.name}"
    
    def update_attendance(self):
        if self.accepted == 1:  # Only update if the document is accepted
            attendance.objects.filter(
                student_id=self.student.id,
                date__range=[self.from_date, self.to_date],
                status=2  # Assuming 2 means 'absent'
            ).update(status=0)  
    
    
            