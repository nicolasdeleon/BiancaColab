# Generated by Django 2.2.5 on 2020-01-11 22:31

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0011_remove_user_birthdate'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='birthDate',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]