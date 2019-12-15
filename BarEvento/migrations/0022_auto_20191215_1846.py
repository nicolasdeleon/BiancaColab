# Generated by Django 2.2.5 on 2019-12-15 21:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('BarEvento', '0021_auto_20191210_2220'),
    ]

    operations = [
        migrations.AlterField(
            model_name='postrelations',
            name='invite_reason',
            field=models.CharField(blank=True, max_length=6),
        ),
        migrations.AlterField(
            model_name='postrelations',
            name='status',
            field=models.CharField(choices=[('W', 'Winner'), ('2BA', 'To_be_accepted'), ('F', 'Finished'), ('R', 'Refused')], default='2BA', max_length=3),
        ),
        migrations.AlterField(
            model_name='postrelations',
            name='winer_code',
            field=models.CharField(max_length=20, verbose_name='Code to Retrieve'),
        ),
    ]
