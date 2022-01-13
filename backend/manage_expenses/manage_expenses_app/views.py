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

class CustomUserCreate(APIView):
    permission_classes = [AllowAny]
    parser_classes = (MultiPartParser, FormParser)

    def post(self, request, format='json'):
        print("request sent")
        result = None
        try:
            serializer = CustomUserCreateSerializser(data=request.data)
            print("request sent")
            if serializer.is_valid(raise_exception=True):
                user = serializer.save()
                print(user)
                if user:
                    user_data = serializer.data
                    result = {
                            "header": getHeader(request_id=user.id, message="User Created Successfully.", status=status.HTTP_200_OK, error_list=[]),
                            "response": user_data
                        }
                    return Response(result, status=status.HTTP_200_OK)
        except Exception as e:
            print(e)
            error_message = str(e)
            if 'email' in error_message:
                result = {
                    "header": getHeader(request_id=None, message="A User with this email already exists, please try with another email.", status=status.HTTP_400_BAD_REQUEST, error_list=[error_message])
                }
            else:
                result = {
                    "header": getHeader(request_id=None, message='please provide complete details', status=status.HTTP_400_BAD_REQUEST, error_list=[error_message])
                }
            return Response(result, status=status.HTTP_400_BAD_REQUEST)
            

