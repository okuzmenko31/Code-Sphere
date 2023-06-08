from django.urls import path, include

urlpatterns = [
    path('users/', include('apps.users.urls')),
    path('tags/', include('apps.tags.urls')),
    path('posts/', include('apps.posts.urls')),
    path('followings/', include('apps.followings.urls')),
    path('notifications/', include('apps.notifications.urls'))
]
