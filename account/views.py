from django.shortcuts import render, redirect
from django.urls import reverse
from .models import Student, Teacher
from django.contrib import messages
from django.contrib.auth import authenticate, login
from .forms import LoginForm
from django.contrib.auth.hashers import make_password
    

def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            id = form.cleaned_data['id']
            password = form.cleaned_data['password']
            role = request.POST['role']
            user = authenticate(request, id=id, password=password, role=role)
            if user is not None:
                login(request, user)
                return redirect('dashboard:dashboard')  
            else:
                messages.error(request, 'Invalid credentials. Please try again.')
                return redirect('account:login')
    else:
        form = LoginForm()
    return render(request, 'account/login.html', {'form': form})

def add_Teacher():
    t = Teacher.objects.create(
        teacher_id='112',
        username='112',
        fullName='Taukekhan',
        email='Taukekhan@sdu.edu.kz'
    )
    t.set_password('happy')
    t.save()

def add_Student():
    s = Student.objects.create(
        student_id='', 
        username='', 
        fullName='', 
        email=''
    )
    s.set_password('your_password')  # Set a password for the student
    s.save()