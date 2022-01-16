# Generated by Django 4.0.1 on 2022-01-16 20:21

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('manage_expenses_app', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='transaction',
            name='created_by',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='owner_of_transaction', to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='transaction',
            name='with_whom',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='with_whom_transaction_is_made', to=settings.AUTH_USER_MODEL),
        ),
    ]
