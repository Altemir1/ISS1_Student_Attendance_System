from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Teacher,Student

class LoginForm(forms.Form):
    id = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'ID'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Password'}))
    
class TeacherCreationForm(UserCreationForm):
    class Meta:
        model = Teacher
        fields = ['id', 'email', 'status']
    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user

class StudentCreationForm(UserCreationForm):
    class Meta:
        model = Student
        fields = ['id', 'email', 'advisor', 'major_program']
    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user
