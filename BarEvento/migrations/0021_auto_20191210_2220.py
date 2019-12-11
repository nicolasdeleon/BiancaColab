# Generated by Django 2.2.5 on 2019-12-11 01:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('BarEvento', '0020_merge_20191210_2220'),
    ]

    operations = [
        migrations.AlterField(
            model_name='barpost',
            name='slug',
            field=models.SlugField(default=1919676576, max_length=255, unique=True),
        ),
        migrations.AlterField(
            model_name='postrelations',
            name='status',
            field=models.CharField(choices=[('Refused', '3'), ('Winner_end', '2'), ('To_be_accepted', '0'), ('Winner_new', '1')], default='To_be_accepted', max_length=1),
        ),
    ]
