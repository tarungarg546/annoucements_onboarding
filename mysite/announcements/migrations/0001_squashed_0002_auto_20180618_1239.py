# -*- coding: utf-8 -*-
# Generated by Django 1.11.13 on 2018-06-18 07:29
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    replaces = [('announcements', '0001_squashed_0007_auto_20180618_1054'), ('announcements', '0002_auto_20180618_1239')]

    initial = True

    dependencies = [
        ('auth', '0008_alter_user_username_max_length'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Announcements',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(help_text=b'This will be shown as the title of notification and announcement', max_length=32)),
                ('message', models.CharField(help_text=b'The message you want to convey', max_length=200)),
                ('date_time_to_publish', models.DateTimeField(help_text=b'Schedule date and time for announcement', verbose_name=b'datetime publish')),
                ('date_time_expire', models.DateTimeField(help_text=b'Expiry date and time for announcement', verbose_name=b'datetime expire')),
                ('groups', models.ManyToManyField(to=b'auth.Group')),
                ('sent_at', models.DateTimeField(blank=True, editable=False, null=True)),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('modified_date', models.DateTimeField(auto_now=True)),
                ('has_expired', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='AnnouncementDeliveryStatus',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.PositiveSmallIntegerField(choices=[(0, b'SEEN'), (1, b'YET TO RECEIVE'), (2, b'EXPIRED'), (3, b'USER LEFT GROUP')])),
                ('announcement', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='announcements.Announcements')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('status_last_update_time', models.DateTimeField(help_text=b'The time at status got updated', verbose_name=b'status last update time')),
            ],
        ),
    ]
