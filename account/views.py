from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Student, Teacher
from django.contrib import messages
from django.contrib.auth import authenticate, login


@login_required
def dashboard(request):
    return render(request,
                  'account/dashboard.html',)

def user_login(request):
    if request.method == 'POST':
        id = request.POST['id']
        password = request.POST['password']
        role = request.POST['role']
        if role == 'student':
            user = authenticate(request, student_id=id, password=password)
            if user is not None:
                login(request, user)
                return redirect('dashboard')
            else:
                messages.error(request, 'Invalid credentials. Please try again.')
        elif role == 'teacher':
            user = authenticate(request, teacher_id=id, password=password)
            if user is not None:
                login(request, user)
                return redirect('dashboard')
            else:
                messages.error(request, 'Invalid credentials. Please try again.')
        elif role == 'admin':
            
            pass
    return render(request, 'account/login.html')

