# Generated by Django 2.2.5 on 2020-01-11 22:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('eventos', '0029_auto_20200111_2217'),
    ]

    operations = [
        migrations.AlterField(
            model_name='eventpost',
            name='status',
            field=models.CharField(choices=[('O', 'Open'), ('2BO', 'To_be_open'), ('C', 'Close'), ('F', 'Finished')], default='2BO', max_length=3),
        ),
        migrations.AlterField(
            model_name='postrelations',
            name='status',
            field=models.CharField(choices=[('R', 'Refused'), ('W', 'Winner'), ('2BA', 'To_be_accepted'), ('F', 'Finished')], default='2BA', max_length=3),
        ),
    ]
