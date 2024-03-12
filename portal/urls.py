from django.contrib import admin
from django.urls import path, include

urlpatterns = [
 path('admin/', admin.site.urls),
 path('', include('dashboard.urls')),
 path('account/', include('account.urls', namespace='account')),
 path('att_registration/',include('attendance.urls'))
]