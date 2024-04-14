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
            
            print(id , password)
            
            user = authenticate(request, id=id, password=password, role=role)
            
            if user is not None:
                login(request, user)
                return redirect('dashboard:student_profile')  
            else:
                messages.error(request, 'Invalid credentials. Please try again and check your role.')
                return redirect('account:login')
    else:
        form = LoginForm()
    return render(request, 'account/login.html', {'form': form})

