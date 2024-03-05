# views.py
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from account.models import Attendance

@csrf_exempt
def register_attendance(request):
    if request.method == 'POST':
        # Extract ID from query parameters
        id = request.POST.get('uid')
        if id:
            attendance = Attendance.objects.create(entity_id=id,course_id="TSS999-1-l-1",really_attended=True)
            if attendance is not None:
                return JsonResponse({'MEW': 'Seccessful'}, status=200)
            else:
                return JsonResponse({'error': 'Unseccessful'}, status=400)
        else:
            return JsonResponse({'error': 'ID parameter is missing.'}, status=400)
    else:
        return JsonResponse({'error': 'Only POST requests are allowed.'}, status=405)
