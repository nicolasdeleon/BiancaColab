# Generated by Django 2.2.5 on 2020-01-17 16:41

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0013_auto_20200111_2321'),
    ]

    operations = [
        migrations.CreateModel(
            name='EmailConfirmed',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('hashkey', models.CharField(max_length=200)),
                ('confirmed', models.BooleanField(default=False)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='accounts.user')),
            ],
        ),
    ]
