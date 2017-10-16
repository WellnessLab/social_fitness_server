# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-10-06 20:26
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('people', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='GroupChallenge',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('duration', models.CharField(choices=[('30m', '30 minutes'), ('1h', 'one hour'), ('2h', 'two hour'), ('12h', 'half day'), ('1d', 'one day'), ('2d', 'two day'), ('3d', 'three day'), ('3d', 'three day'), ('7d', 'one week')], max_length=16)),
                ('start_datetime', models.DateTimeField()),
                ('end_datetime', models.DateTimeField()),
                ('completed_datetime', models.DateTimeField()),
                ('group', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='people.Group')),
            ],
        ),
        migrations.CreateModel(
            name='Level',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order', models.IntegerField()),
                ('name', models.CharField(max_length=128)),
                ('goal', models.IntegerField()),
                ('goal_is_percent', models.BooleanField(default=True)),
                ('unit', models.CharField(choices=[('steps', 'steps'), ('minutes', 'minutes'), ('minutes_moderate', 'minutes in moderate'), ('minutes_vigorous', 'minutes in vigorous'), ('distance', 'distance')], max_length=32)),
                ('unit_duration', models.CharField(choices=[('30m', '30 minutes'), ('1h', 'one hour'), ('2h', 'two hour'), ('12h', 'half day'), ('1d', 'one day'), ('2d', 'two day'), ('3d', 'three day'), ('3d', 'three day'), ('7d', 'one week')], max_length=16)),
                ('total_duration', models.CharField(choices=[('30m', '30 minutes'), ('1h', 'one hour'), ('2h', 'two hour'), ('12h', 'half day'), ('1d', 'one day'), ('2d', 'two day'), ('3d', 'three day'), ('3d', 'three day'), ('7d', 'one week')], max_length=16)),
                ('subgoal_1', models.IntegerField()),
                ('subgoal_2', models.IntegerField()),
                ('subgoal_3', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='LevelGroup',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=32)),
            ],
        ),
        migrations.CreateModel(
            name='PersonChallenge',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('unit', models.CharField(choices=[('steps', 'steps'), ('minutes', 'minutes'), ('minutes_moderate', 'minutes in moderate'), ('minutes_vigorous', 'minutes in vigorous'), ('distance', 'distance')], max_length=32)),
                ('unit_goal', models.IntegerField()),
                ('unit_duration', models.CharField(choices=[('30m', '30 minutes'), ('1h', 'one hour'), ('2h', 'two hour'), ('12h', 'half day'), ('1d', 'one day'), ('2d', 'two day'), ('3d', 'three day'), ('3d', 'three day'), ('7d', 'one week')], max_length=16)),
                ('group_challenge', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='challenges.GroupChallenge')),
                ('level', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='challenges.Level')),
                ('person', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='people.Person')),
            ],
        ),
        migrations.CreateModel(
            name='PersonFitnessMilestone',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_datetime', models.DateTimeField()),
                ('end_datetime', models.DateTimeField()),
                ('steps', models.IntegerField()),
                ('calories', models.FloatField()),
                ('active_minutes', models.IntegerField()),
                ('active_minutes_moderate', models.IntegerField()),
                ('active_minutes_vigorous', models.IntegerField()),
                ('distance', models.FloatField()),
                ('person', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='people.Person')),
            ],
        ),
        migrations.AddField(
            model_name='level',
            name='group',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='challenges.LevelGroup'),
        ),
    ]