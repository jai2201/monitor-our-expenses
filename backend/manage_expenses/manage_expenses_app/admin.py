from django.contrib import admin
from django.contrib import auth
from django.contrib.auth.models import Group
from .models import BaseUserProfile

admin.site.register(BaseUserProfile)