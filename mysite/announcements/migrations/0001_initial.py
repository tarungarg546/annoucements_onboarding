# -*- coding: utf-8 -*-
# Generated by Django 1.11.13 on 2018-06-04 06:15
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Annoucements',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('message', models.CharField(max_length=200)),
                ('date_published', models.DateTimeField(verbose_name=b'date published')),
                ('date_expire', models.DateTimeField(verbose_name=b'date expire')),
            ],
        ),
    ]
