# Generated by Django 2.2.5 on 2019-12-02 21:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('BarEvento', '0012_auto_20191124_1038'),
    ]

    operations = [
        migrations.AlterField(
            model_name='barpost',
            name='slug',
            field=models.SlugField(default=140718231165264, max_length=255, unique=True),
        ),
    ]
