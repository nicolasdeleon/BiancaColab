# Generated by Django 2.2.5 on 2019-12-06 00:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('BarEvento', '0014_auto_20191203_2136'),
    ]

    operations = [
        migrations.AlterField(
            model_name='barpost',
            name='slug',
            field=models.SlugField(default=1922953376, max_length=255, unique=True),
        ),
    ]