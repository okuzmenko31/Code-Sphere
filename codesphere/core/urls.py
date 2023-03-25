from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('codesphere/welcome/', include('home.urls')),
    path('codesphere/tags/', include('tags.urls'))
]
