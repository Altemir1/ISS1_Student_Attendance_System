from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .forms import LoginForm

@login_required
def dashboard(request):
    return render(request,
                  'account/dashboard.html',
                  {'section': 'dashboard'})

def user_login(request):
    

    return render(request, 'account/login.html', )

