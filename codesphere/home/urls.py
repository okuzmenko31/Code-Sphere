from django.urls import path
from .views import *

urlpatterns = [
    path('', WelcomePage.as_view(), name='welcome-page'),
    path('test/', test_view, name='test')
]
