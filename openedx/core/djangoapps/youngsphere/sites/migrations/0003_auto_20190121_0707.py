# -*- coding: utf-8 -*-
# Generated by Django 1.11.15 on 2019-01-21 12:07
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('youngsphere_sites', '0002_auto_20190121_0603'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='school',
            name='site',
        ),
        migrations.AddField(
            model_name='school',
            name='schoolname',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
    ]
