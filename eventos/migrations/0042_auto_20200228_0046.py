# Generated by Django 2.2.5 on 2020-02-28 00:46

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('eventos', '0041_auto_20200228_0045'),
    ]

    operations = [
        migrations.AlterField(
            model_name='instastorypublication',
            name='person',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounts.user'),
        ),
    ]