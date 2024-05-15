from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login
from .forms import LoginForm
from django.views.decorators.cache import never_cache


@never_cache
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
                if user.is_student:
                    return redirect('dashboard:student_profile')
                else:
                    return redirect('dashboard:teacher_profile')  
            else:
                messages.error(request, 'Invalid credentials. Please try again and check your role.')
                return redirect('account:login')
    else:
        form = LoginForm()
    return render(request, 'account/login.html', {'form': form})

@never_cache
def admin_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            id = form.cleaned_data['id']
            password = form.cleaned_data['password']
            
            # Assuming `authenticate_admin` is a method in your custom backend.
            user = authenticate(request, id=id, password=password, role='admin')
            
            if user is not None and user.is_admin:  # Ensure the user is indeed an admin.
                login(request, user)
                return redirect('dashboard:admin_dashboard')  # Redirect to the admin dashboard.
            else:
                messages.error(request, 'Invalid credentials or not authorized as admin.')
                return redirect('account:adminka')  # Redirect back to admin login page if authentication fails.
        else:
            messages.error(request, 'Invalid form submission.')
            return redirect('account:adminka')
    else:
        form = LoginForm()

    return render(request, 'account/adminka.html', {'form': form})