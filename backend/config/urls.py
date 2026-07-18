from django.contrib import admin
from django.urls import path, include

# Urls for the hardware app
urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('apps.hardware.urls')),
]
