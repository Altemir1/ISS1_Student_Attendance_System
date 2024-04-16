from django import forms
from django.core.exceptions import ValidationError

def validate_file_extension(value):
    if not value.name.endswith('.pdf'):
        raise ValidationError('Only PDF files are allowed.')


class DocumentSubmissionForm(forms.Form):
    description = forms.CharField(widget=forms.Textarea(attrs={'rows': 4}), required=True)
    document = forms.FileField(required=True,validators=[validate_file_extension])