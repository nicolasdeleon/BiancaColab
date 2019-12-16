# Generated by Django 2.2.5 on 2019-12-16 02:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('BarEvento', '0024_auto_20191215_2259'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='postrelations',
            name='winner_code',
        ),
        migrations.AlterField(
            model_name='postrelations',
            name='status',
            field=models.CharField(choices=[('R', 'Refused'), ('W', 'Winner'), ('F', 'Finished'), ('2BA', 'To_be_accepted')], default='2BA', max_length=3),
        ),
    ]
