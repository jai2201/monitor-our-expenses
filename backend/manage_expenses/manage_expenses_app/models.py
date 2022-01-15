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
    profile_picture = models.ImageField(upload_to='media/profile_picures', null=True, blank=True)
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

class UserQueries(models.Model):
    email = models.EmailField()
    query = models.CharField(max_length=1000)
    is_solved = models.BooleanField(default=False)

    def __str__(self):
        return str(self.id) + ' : ' + self.email