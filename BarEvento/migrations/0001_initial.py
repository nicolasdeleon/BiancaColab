# Generated by Django 2.2.5 on 2019-11-23 19:15

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Fotos',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.FileField(blank=True, null=True, upload_to='image/')),
                ('updloader', models.ForeignKey(blank=True, default=1, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='BarPost',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=30)),
                ('company', models.CharField(max_length=30)),
                ('slug', models.SlugField(default=140704070867280, max_length=255, unique=True)),
                ('desc', models.CharField(blank=True, max_length=255, null=True)),
                ('createTime', models.DateTimeField(auto_now=True)),
                ('dia', models.TextField()),
                ('code', models.CharField(max_length=5, null=True)),
                ('is_finalized', models.TextField(blank=True, null=True)),
                ('posts', models.ManyToManyField(blank=True, to='BarEvento.Fotos', verbose_name='publicaciones')),
                ('users', models.ManyToManyField(blank=True, to=settings.AUTH_USER_MODEL, verbose_name='list of users')),
            ],
            options={
                'ordering': ['-createTime'],
            },
        ),
    ]
