from django.contrib import admin
from django.contrib import auth
from django.contrib.auth.models import Group
from .models import BaseUserProfile, UserQueries, Expense, ExpensesGroup, Comment, UserQueries, Transaction

admin.site.register(BaseUserProfile)
admin.site.register(Expense)
admin.site.register(ExpensesGroup)
admin.site.register(Comment)
admin.site.register(UserQueries)
admin.site.register(Transaction)