from django import forms

class LoginForm(forms.Form):
    id = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'ID'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Password'}))
    
