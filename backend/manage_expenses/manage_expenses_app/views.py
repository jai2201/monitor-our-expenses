from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny , IsAuthenticated
from .serializers import CustomUserCreateSerializser
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
                    try:
                        registered_user = BaseUserProfile.objects.get(
                            email=user_data['email'])
                        token = RefreshToken.for_user(
                            registered_user).access_token

                        subject = "Verify your Email with us | Royal Split of Spain"
                        verify_link = settings.DEFAULT_HOST + '/verify-email/' + str(token) +'/'
                        print(verify_link,"verify link")
                        print("access token", token)
                        html_message = loader.render_to_string(
                            'email_verification.html',
                            {
                                'user_name': user.fullname,
                                'verify_link': verify_link
                            }
                        )
                        send_mail(subject=subject, message='', from_email=settings.EMAIL_HOST_USER ,  recipient_list=[registered_user.email], fail_silently=False, html_message=html_message)
                        result = {
                                "header": getHeader(request_id=user.id, message="User Created Successfully.", status=status.HTTP_200_OK, error_list=[]),
                                "response": user_data
                            }
                        return Response(result, status=status.HTTP_200_OK)
                    except Exception as e:
                        result = {
                            "header": getHeader(request_id=None, message='Unable to send email, Please enter a valid email and try again', status=status.HTTP_400_BAD_REQUEST, error_list=[error_message])
                        }
                        return Response(result, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            print(e)
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
                    "header": getHeader(request_id=None, message='please provide complete details', status=status.HTTP_400_BAD_REQUEST, error_list=[error_message])
                }
            return Response(result, status=status.HTTP_400_BAD_REQUEST)
            

class VerifyEmail(APIView):
    permission_classes = [AllowAny]

    def get(self,request,verification_token):
        print("REQUEST SENT")
        token = verification_token
        print("FROM EMAIL",token)
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=["HS256"])
        print(payload)
        try:
            user = BaseUserProfile.objects.get(id=payload['user_id'])
            print(user)
            user.is_email_verified = True
            user.save()
            login(request, user)
            return HttpResponse('Your account has been confirmed')
        except Exception as e:
            print(e)
            return HttpResponse('Invalid token. Please contact the admin.')

# class ResendEmailVerification(APIView):
