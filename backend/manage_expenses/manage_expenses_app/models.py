from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import AbstractBaseUser , PermissionsMixin
from .managers import CustomUserManager
from django.conf import settings
from .constants import GROUP_TYPE_CHOICES, SPLIT_TYPE, TRANSACTION_TYPE
# need to import Program model


class BaseUserProfile(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    fullname = models.CharField(max_length=50)
    profile_picture = models.ImageField(upload_to='profile_picures', null=True, blank=True)
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

class Expense(models.Model):
    total_amount = models.IntegerField(default=0)
    description = models.CharField(max_length=1000)
    split_type = models.CharField(max_length=100, choices=SPLIT_TYPE)
    # with_whom_to_split = models.ForeignKey(BaseUserProfile, on_delete=models.CASCADE,related_name="with_whom_to_split")
    # amount_you_have_to_pay = models.IntegerField(default=0)
    # amount_you_will_receive = models.IntegerField(default=0)
    who_has_paid = models.ManyToManyField('BaseUserProfile', related_name='who_all_has_paid')
    with_whom_to_split = models.ManyToManyField('BaseUserProfile', related_name='with_whom_to_split')
    date = models.DateTimeField(auto_now_add=True)
    note = models.CharField(max_length=500, null=True, blank=True)
    added_by = models.ForeignKey(BaseUserProfile, on_delete=models.CASCADE, related_name="added_by")
    is_setteled = models.BooleanField(default=False)

class Transaction(models.Model):
    created_by = models.ForeignKey(BaseUserProfile, on_delete=models.CASCADE, related_name='owner_of_transaction')
    with_whom = models.ForeignKey(BaseUserProfile, on_delete=models.CASCADE, related_name='with_whom_transaction_is_made')
    type_of_transaction = models.CharField(max_length=100, default='TO_PAY' , choices=TRANSACTION_TYPE)
    amount_to_exchange = models.IntegerField(default=0)
    expense = models.ForeignKey(Expense, on_delete=models.CASCADE)

class ExpensesGroup(models.Model):
    group_name = models.CharField(max_length=100)
    group_type = models.CharField(max_length=200, choices=GROUP_TYPE_CHOICES, default='Friends')
    members = models.ManyToManyField('BaseUserProfile', blank=False, related_name='groups_list')
    expenses = models.ManyToManyField('Expense',blank=True, related_name='groups_list_for_this_expense')
    group_picture = models.ImageField(upload_to='group_pictures',null=True,blank=True)

class Comment(models.Model):
    comment_message = models.CharField(max_length=1000)
    commented_by = models.ForeignKey(BaseUserProfile, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    expense = models.ForeignKey(Expense, on_delete=models.CASCADE)

class UserQueries(models.Model):
    email = models.EmailField()
    query = models.CharField(max_length=1000)
    is_solved = models.BooleanField(default=False)

    def __str__(self):
        return str(self.id) + ' : ' + self.email