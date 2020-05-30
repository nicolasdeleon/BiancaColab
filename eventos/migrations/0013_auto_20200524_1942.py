# Generated by Django 3.0.4 on 2020-05-24 22:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('eventos', '0012_post_exchange_code'),
    ]

    operations = [
        migrations.AddField(
            model_name='instastorypublication',
            name='processedImage',
            field=models.ImageField(blank=True, null=True, upload_to='processed/'),
        ),
        migrations.AlterField(
            model_name='event',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='events/'),
        ),
        migrations.AlterField(
            model_name='instastorypublication',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='to_process/'),
        ),
    ]