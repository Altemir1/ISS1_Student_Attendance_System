from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model

class CustomUserBackend(ModelBackend):
    def authenticate(self, request, id=None, password=None, **kwargs):
        UserModel = get_user_model()
        try:
            user = UserModel.objects.get(student__student_id=id)
        except UserModel.DoesNotExist:
            try:
                user = UserModel.objects.get(teacher__teacher_id=id)
            except UserModel.DoesNotExist:
                return None

        if kwargs['role'] == 'student' and not user.is_student:
            return None 
        elif kwargs['role'] == 'teacher' and not user.is_teacher:
            return None 
        
        
        if user.check_password(password):
            print(f"User authenticated: {user}")
            return user

        return None
