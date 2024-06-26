from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import check_password

class CustomUserBackend(ModelBackend):
    def authenticate(self, request, id=None, password=None, **kwargs):
        
        UserModel = get_user_model()
        
        try:
            user = UserModel.objects.get(student__id=id)
        except UserModel.DoesNotExist:
            try:
                user = UserModel.objects.get(teacher__id=id)
            except UserModel.DoesNotExist:
                return None
        
        if kwargs['role'] == 'student' and not user.is_student:
            return None 
        
        elif kwargs['role'] == 'teacher' and not user.is_teacher:
            return None 
        
        if check_password(password, user.password):
            print(f"User authenticated: {user}")
            return user

        return None
    
    def authenticate_admin(self, request, id=None, password=None, **kwargs):
        UserModel = get_user_model()
        
        try:
            user = UserModel.objects.get(admin__id=id)
        except UserModel.DoesNotExist:
            return None
        
        # Here we assume 'is_admin' is an attribute to check if the user is an admin
        if not user.is_admin:
            return None
        
        if check_password(password, user.password):
            print(f"Admin authenticated: {user}")
            return user
        
        return None