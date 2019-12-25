# Generated by Django 2.2.5 on 2019-12-25 22:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('eventos', '0002_auto_20191225_1605'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='eventpost',
            name='is_finalized',
        ),
        migrations.AddField(
            model_name='eventpost',
            name='status',
            field=models.CharField(choices=[('C', 'Close'), ('2BO', 'To_be_open'), ('F', 'Finished'), ('O', 'Open')], default='O', max_length=3),
        ),
        migrations.AlterField(
            model_name='postrelations',
            name='status',
            field=models.CharField(choices=[('W', 'Winner'), ('R', 'Refused'), ('F', 'Finished'), ('2BA', 'To_be_accepted')], default='2BA', max_length=3),
        ),
    ]
