# Generated by Django 3.0.5 on 2020-05-13 21:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('eventos', '0009_auto_20200513_1830'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='slug',
            field=models.SlugField(max_length=255),
        ),
    ]
