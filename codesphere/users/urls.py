from django.urls import path
from .views import *

urlpatterns = [
    path('submit_email_signup/',
         SubmitRegistrationEmail.as_view(),
         name='submit_email_signup'),
    path('signup/<token>/<email>/', ConfirmEmailAndRegister.as_view(), name='confirm_email_register'),
    path('signin/', SignIn.as_view(), name='signin')
]
