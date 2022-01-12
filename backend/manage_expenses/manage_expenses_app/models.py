from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import AbstractBaseUser , PermissionsMixin
from .managers import CustomUserManager
from django.conf import settings
# need to import Program model


class BaseUserProfile(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    fullname = models.CharField(max_length=50)
    profile_picture = models.ImageField(upload_to='profile_picures', null=False , blank=False)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)  
    is_email_verified = models.BooleanField(default=False)
    # login using email
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    # default UserManager
    objects = CustomUserManager()

    def __str__(self):
        return "PK: " + str(self.pk) + " | " + self.email

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, module):
        authorized_list = ['auth'] + ['manage_expenses_app']
        if module in authorized_list and self.is_admin:
            return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin
    
    @property
    def default_profile_picture(self):
        if self.profile_picture:
            return "%s/%s" %(settings.MEDIA_URL, self.profile_picture)
        else:
            return settings.STATIC_URL + 'img/default_profile_picture.jpg'
