from django.db import models
from account.models import CustomUser
# Create your models here.

class SubmittedDocument(models.Model):
    student = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="documents")
    description = models.TextField()
    document = models.FileField(upload_to='student_documents/')
    submitted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.student.id} -  {self.document.name}"