# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-06-12 18:49
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('people', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Account',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fullname', models.CharField(max_length=200)),
                ('user_id', models.CharField(max_length=50, unique=True)),
                ('access_token', models.CharField(max_length=1000)),
                ('refresh_token', models.CharField(max_length=1000)),
                ('expires_at', models.DateTimeField(blank=True, null=True)),
                ('last_pull_time', models.DateTimeField(blank=True, default=datetime.datetime(2017, 5, 1, 0, 0), null=True)),
                ('device_version', models.CharField(max_length=64)),
                ('person', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='people.Person')),
            ],
        ),
    ]