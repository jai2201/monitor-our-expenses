from os import name
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from .views import (
    CustomUserCreate, VerifyEmail, ResendEmailVerification, ChangePassword, SendForgotPasswordEmail, ResetForgotPassword, UpdateBaseUserProfile
)

urlpatterns = [
    path('register/', CustomUserCreate.as_view(), name="register"),
    path('verify-email/<str:verification_token>/', VerifyEmail.as_view(), name="verify_email"),
    path('resend-email-verification/',ResendEmailVerification.as_view(), name="resend_email_verification"),
    path('change-password/', ChangePassword.as_view(), name="change-password"),
    path('forgot-password/', SendForgotPasswordEmail.as_view(), name="send_forgot_password_email"),
    path('forgot-password/<str:verification_token>/', ResetForgotPassword.as_view(), name="reset_forgot_password"),
    path('update-user-profile/', UpdateBaseUserProfile.as_view(), name="update_user_profile")
]