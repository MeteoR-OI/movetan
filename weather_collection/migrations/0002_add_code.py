# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-05-17 16:49
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('weather_collection', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='site',
            name='code',
            field=models.CharField(default='', max_length=10, unique=True),
            preserve_default=False,
        ),
    ]