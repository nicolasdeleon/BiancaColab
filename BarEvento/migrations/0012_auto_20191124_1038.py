# Generated by Django 2.2.5 on 2019-11-24 13:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('BarEvento', '0011_auto_20191124_1029'),
    ]

    operations = [
        migrations.AlterField(
            model_name='barpost',
            name='is_finalized',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='barpost',
            name='slug',
            field=models.SlugField(default=140703699278160, max_length=255, unique=True),
        ),
    ]
