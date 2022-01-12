from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny


class CustomUserCreate(APIView):
    permission_classes = [AllowAny]
    pass
