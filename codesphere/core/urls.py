from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from allauth.socialaccount.views import SignupView as SocialSignupView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('mdeditor/', include('mdeditor.urls')),
    path('accounts/', include('allauth.urls')),
    path('codesphere/user/', include('users.urls')),
    path('codesphere/welcome/', include('home.urls')),
    path('codesphere/tags/', include('tags.urls')),
    path('codesphere/posts/', include('posts.urls'))
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
