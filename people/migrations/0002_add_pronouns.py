# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-10-10 17:59
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion

def load_pronouns_from_fixture(apps, schema_editor):
    from django.core.management import call_command
    call_command("loaddata", "pronouns")


def delete_pronouns(apps, schema_editor):
    Store = apps.get_model("people", "Pronoun")
    Store.objects.all().delete()


class Migration(migrations.Migration):

    dependencies = [
        ('people', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Pronoun',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('personal', models.CharField(default='personal', max_length=16)),
                ('pronoun', models.CharField(default='pronoun', max_length=16)),
                ('possessive', models.CharField(default='possessive', max_length=16)),
            ],
        ),
        migrations.RunPython(load_pronouns_from_fixture, delete_pronouns),
        migrations.AddField(
            model_name='membership',
            name='pronoun',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='people.Pronoun'),
        ),
    ]