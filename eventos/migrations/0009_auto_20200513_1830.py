# Generated by Django 3.0.5 on 2020-05-13 21:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('eventos', '0008_auto_20200511_1948'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='slug',
            field=models.SlugField(max_length=255, unique=True),
        ),
    ]
