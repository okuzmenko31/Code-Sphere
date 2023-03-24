from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('tech-sphere/welcome/', include('home.urls'))
]
