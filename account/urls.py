from django.urls import path, include
from django.contrib.auth import views as auth_views
from . import views
from django.conf import settings

app_name = 'account'
urlpatterns = [
    path('login/', views.user_login, name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page=settings.LOGOUT_REDIRECT_URL), name='logout'),   
]