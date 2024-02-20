from django import forms

class LoginForm(forms.Form):
    id = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)
    