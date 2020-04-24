# Generated by Django 3.0.5 on 2020-04-24 14:19

import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0004_auto_20200423_0030'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='eventWatchList',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.CharField(blank=True, default='0', max_length=30), blank=True, default=list, size=50),
        ),
        migrations.AddField(
            model_name='profile',
            name='notificationToken',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
