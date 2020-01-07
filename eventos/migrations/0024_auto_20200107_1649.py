# Generated by Django 2.2.5 on 2020-01-07 16:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('eventos', '0023_auto_20200107_1619'),
    ]

    operations = [
        migrations.AlterField(
            model_name='eventpost',
            name='status',
            field=models.CharField(choices=[('2BO', 'To_be_open'), ('O', 'Open'), ('C', 'Close'), ('F', 'Finished')], default='2BO', max_length=3),
        ),
        migrations.AlterField(
            model_name='postrelations',
            name='notificationToken',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='postrelations',
            name='status',
            field=models.CharField(choices=[('2BA', 'To_be_accepted'), ('R', 'Refused'), ('W', 'Winner'), ('F', 'Finished')], default='2BA', max_length=3),
        ),
    ]
