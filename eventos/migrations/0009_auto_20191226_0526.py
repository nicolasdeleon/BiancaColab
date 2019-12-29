# Generated by Django 2.2.5 on 2019-12-26 05:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('eventos', '0008_auto_20191225_2112'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='postrelations',
            name='code',
        ),
        migrations.AlterField(
            model_name='eventpost',
            name='code',
            field=models.CharField(max_length=5, null=True, unique=True),
        ),
        migrations.AlterField(
            model_name='eventpost',
            name='slug',
            field=models.SlugField(default=8532160, max_length=255, unique=True),
        ),
        migrations.AlterField(
            model_name='eventpost',
            name='status',
            field=models.CharField(choices=[('O', 'Open'), ('F', 'Finished'), ('2BO', 'To_be_open'), ('C', 'Close')], default='2BO', max_length=3),
        ),
        migrations.AlterField(
            model_name='postrelations',
            name='status',
            field=models.CharField(choices=[('F', 'Finished'), ('R', 'Refused'), ('W', 'Winner'), ('2BA', 'To_be_accepted')], default='2BA', max_length=3),
        ),
    ]