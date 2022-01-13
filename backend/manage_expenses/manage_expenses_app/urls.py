from os import name
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from .views import (
    CustomUserCreate, VerifyEmail, ResendEmailVerification
)

urlpatterns = [
    path('register/', CustomUserCreate.as_view(), name="register"),
    path('verify-email/<str:verification_token>/', VerifyEmail.as_view(), name="verify_email"),
    path('resend-email-verification/',ResendEmailVerification.as_view(), name="resend_email_verification"),
]