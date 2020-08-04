# Generated by Django 3.0 on 2020-08-03 16:10

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
            name='Profile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('phone', models.CharField(blank=True, max_length=20, verbose_name='电话')),
                ('avatar', models.ImageField(blank=True, upload_to='avatar/%Y%m%d/', verbose_name='头像')),
                ('bio', models.TextField(blank=True, max_length=500, verbose_name='个人简介')),
                ('mod_date', models.DateTimeField(auto_now=True, verbose_name='最后确认时间')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='profile', to=settings.AUTH_USER_MODEL, verbose_name='用户')),
            ],
            options={
                'verbose_name': '个人信息',
                'verbose_name_plural': '个人信息',
            },
        ),
    ]