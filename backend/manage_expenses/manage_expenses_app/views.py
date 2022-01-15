from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny , IsAuthenticated
from .serializers import CustomUserCreateSerializser, ChangePasswordSerializer, ForgotPasswordSerializer
from rest_framework.response import Response
from django.db import transaction
from django.http.request import HttpRequest
from django.http.response import HttpResponse
from django.shortcuts import render, redirect
from .common_utils import getHeader
from rest_framework import status
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework_simplejwt.authentication import JWTTokenUserAuthentication
from rest_framework_simplejwt.tokens import RefreshToken
from django.core.mail import send_mail
from .models import BaseUserProfile
from django.conf import settings
import jwt
from django.contrib import messages
from django.template import loader
from django.contrib.auth import authenticate, login
import json
from rest_framework import generics

class CustomUserCreate(APIView):
    permission_classes = [AllowAny]
    parser_classes = (MultiPartParser, FormParser)

    def post(self, request, format='json'):
        result = None
        try:
            serializer = CustomUserCreateSerializser(data=request.data)
            if serializer.is_valid(raise_exception=True):
                user = serializer.save()
                if user:
                    user_data = serializer.data
                    registered_user = BaseUserProfile.objects.get(
                        email=user_data['email'])
                    token = RefreshToken.for_user(
                        registered_user).access_token

                    subject = "Verify your Email with us | Royal Split of Spain"
                    verify_link = settings.DEFAULT_HOST + '/verify-email/' + str(token) +'/'
                    html_message = loader.render_to_string(
                        'email_verification.html',
                        {
                            'user_name': user.fullname,
                            'verify_link': verify_link
                        }
                    )
                    try:
                        send_mail(subject=subject, message='', from_email=settings.EMAIL_HOST_USER ,  recipient_list=[registered_user.email], fail_silently=False, html_message=html_message)
                        result = {
                                "header": getHeader(request_id=user.id, message="User created successfully, Please verifiy your account with an email sent to it and login.", status=status.HTTP_200_OK, error_list=[]),
                                "response": user_data
                            }
                        return Response(result, status=status.HTTP_200_OK)
                    except Exception as e:
                        error_message = str(e)
                        result = {
                            "header": getHeader(request_id=None, message='User created successfully but failed to send Verification email, please retry sending verification email.', status=status.HTTP_500_INTERNAL_SERVER_ERROR, error_list=[error_message])
                        }
                        return Response(result, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            error_message = str(e)
            if 'email' in error_message:
                result = {
                    "header": getHeader(request_id=None, message="A User with this email already exists, please try with another email.", status=status.HTTP_400_BAD_REQUEST, error_list=[error_message])
                }
            elif 'password' in error_message:
                result = {
                    "header": getHeader(request_id=None, message='Please enter a valid password (with a minimum length of 8)', status=status.HTTP_400_BAD_REQUEST, error_list=[error_message])
                }
            else:
                result = {
                    "header": getHeader(request_id=None, message='Please provide complete details', status=status.HTTP_400_BAD_REQUEST, error_list=[error_message])
                }
            return Response(result, status=status.HTTP_400_BAD_REQUEST)
            

class VerifyEmail(APIView):
    permission_classes = [AllowAny]
    result = None
    def get(self,request,verification_token):
        token = verification_token
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=["HS256"])
        try:
            user = BaseUserProfile.objects.get(id=payload['user_id'])
            user.is_email_verified = True
            user.save()
            login(request, user)
            result = {
                    "header": getHeader(request_id=user.id, message='User verified Successfully.', status=status.HTTP_200_OK, error_list=[])
                }
            return Response(result, status=status.HTTP_200_OK)
        except Exception as e:
            result = {
                    "header": getHeader(request_id=None, message='Invalid token. Please contact the admin.', status=status.HTTP_400_BAD_REQUEST, error_list=[error_message])
                }
            return Response(result, status=status.HTTP_400_BAD_REQUEST)


class ResendEmailVerification(APIView):
    permission_classes=[AllowAny]


    def post(self, request, format='json'):
        request_body = request.data
        result = None
        try:
            email = request_body['email']
            user = BaseUserProfile.objects.get(email=serializer_data['email'])
            if not user.is_email_verified:
                token = RefreshToken.for_user(user).access_token
                subject = "Verify your Email with us | Royal Split of Spain"
                verify_link = settings.DEFAULT_HOST + '/verify-email/' + str(token) +'/'
                html_message = loader.render_to_string(
                    'email_verification.html',
                    {
                        'user_name': user.fullname,
                        'verify_link': verify_link
                    }
                )
                try:
                    send_mail(subject=subject, message='', from_email=settings.EMAIL_HOST_USER ,  recipient_list=[user.email], fail_silently=False, html_message=html_message)
                    result = {
                        "header": getHeader(request_id=user.id, message="Verification Email resent Successfully.", status=status.HTTP_200_OK, error_list=[]),
                    }
                    return Response(result, status=status.HTTP_200_OK)
                except Exception as e:
                    error_message = str(e)
                    result = {
                        "header": getHeader(request_id=None, message="Failed to send email, Please try again.", status=status.HTTP_400_BAD_REQUEST, error_list=[error_message]),
                    }
                    return Response(result, status=status.HTTP_400_BAD_REQUEST)
            else:
                result = {
                    "header": getHeader(request_id=user.id, message="User is already email verified, Please login directly.", status=status.HTTP_200_OK, error_list=[]),
                }
                return Response(result, status=status.HTTP_200_OK)
        except Exception as e:
            error_message = str(e)
            result = {
                "header": getHeader(request_id=None, message="An account with this email does not exists, Please enter a valid email.", status=status.HTTP_400_BAD_REQUEST, error_list=[error_message]),
            }
            return Response(result, status=status.HTTP_400_BAD_REQUEST)


class ChangePassword(APIView):
    permission_classes = [IsAuthenticated]

    def post(self,request):
        result = None
        try:
            user = request.user
            serializer = ChangePasswordSerializer(data=request.data, context={'user': user})
            if serializer.is_valid(raise_exception=True):
                user.set_password(request.data['new_password'])
                user.save()
                result = {
                    "header": getHeader(request_id=user.id, message='Password Changed Successfully', status=status.HTTP_200_OK, error_list=[])
                }
                return Response(result, status=status.HTTP_200_OK)
        except Exception as e:
            error_message = str(e)
            if 'old_password' in error_message:
                result = {
                    "header": getHeader(request_id=None, message="Please enter your correct old password." , status=status.HTTP_400_BAD_REQUEST, error_list=[error_message])
                }
                return Response(result, status=status.HTTP_400_BAD_REQUEST)
            elif 'new_password' in error_message:
                result = {
                    "header": getHeader(request_id=None, message="Please Enter a Valid Password ensuring at least 8 characters." , status=status.HTTP_400_BAD_REQUEST, error_list=[error_message])
                }
                return Response(result, status=status.HTTP_400_BAD_REQUEST)
            elif 'non_field_errors' in error_message:
                result = {
                    "header": getHeader(request_id=None, message="Your New Password and confirm Password don't match." , status=status.HTTP_400_BAD_REQUEST, error_list=[error_message])
                }
                return Response(result, status=status.HTTP_400_BAD_REQUEST)


class SendForgotPasswordEmail(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        email = request.data['email']
        try:
            user = BaseUserProfile.objects.get(email=email)
            verification_token = RefreshToken.for_user(user).access_token
            forgot_password_link = settings.DEFAULT_HOST + '/forgot-password/' + str(verification_token) +'/'
            subject = 'Forgot Password'
            html_message = loader.render_to_string(
                'forgot_password.html',
                {
                    'user_name': user.fullname,
                    'verify_link': forgot_password_link
                }
            )
            try:
                send_mail(subject=subject, message='', from_email=settings.EMAIL_HOST_USER ,  recipient_list=[user.email], fail_silently=False, html_message=html_message)
                result = {
                        "header": getHeader(request_id=user.id, message="Reset Password Email sent Successfully.", status=status.HTTP_200_OK, error_list=[]),
                    }
                return Response(result, status=status.HTTP_200_OK)
            except Exception as e:
                error_message = str(e)
                result = {
                    "header": getHeader(request_id=None, message='Failed to send Reset Password Email, Please try again.', status=status.HTTP_500_INTERNAL_SERVER_ERROR, error_list=[error_message])
                }
                return Response(result, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            error_message=str(e)
            result = {
                "header":getHeader(request_id=None, message='A Registered User with this Email does not exist, Please enter a valid email or register yourself', status=status.HTTP_400_BAD_REQUEST, error_list=[error_message])
            }
            return Response(result, status=status.HTTP_400_BAD_REQUEST)


class ResetForgotPassword(generics.UpdateAPIView):
    permission_classes = [AllowAny]

    def post(self, request,verification_token,format='json'):
        token = verification_token
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=["HS256"])
        try:
            user = BaseUserProfile.objects.get(id=payload['user_id'])
            if request.data['new_password'] == request.data['confirm_password']:
                user.set_password(request.data['new_password'])
                user.save()
                result = {
                    "header": getHeader(request_id=user.id, message='Password Set Successfully', status=status.HTTP_200_OK, error_list=[])
                }
                return Response(result, status=status.HTTP_200_OK)
            else:
                result = {
                    "header": getHeader(request_id=user.id, message="New and Confirm password didn't match.", status=status.HTTP_400_BAD_REQUEST, error_list=[])
                }
                return Response(result, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            print(e)
            error_message=str(e)
            result = {
                "header":getHeader(request_id=None, message='Invalid Token, Please Try again', status=status.HTTP_400_BAD_REQUEST,error_list=[error_message])
            }
            return Response(result, status=status.HTTP_400_BAD_REQUEST)