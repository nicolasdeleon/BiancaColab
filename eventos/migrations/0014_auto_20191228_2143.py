# Generated by Django 2.2.5 on 2019-12-29 00:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('eventos', '0013_auto_20191228_2140'),
    ]

    operations = [
        migrations.AlterField(
            model_name='eventpost',
            name='status',
            field=models.CharField(choices=[('C', 'Close'), ('F', 'Finished'), ('O', 'Open'), ('2BO', 'To_be_open')], default='O', max_length=3),
        ),
        migrations.AlterField(
            model_name='postrelations',
            name='status',
            field=models.CharField(choices=[('R', 'Refused'), ('F', 'Finished'), ('2BA', 'To_be_accepted'), ('W', 'Winner')], default='2BA', max_length=3),
        ),
    ]