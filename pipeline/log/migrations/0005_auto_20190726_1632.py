# -*- coding: utf-8 -*-
# Generated by Django 1.11.11 on 2019-07-26 08:32
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('log', '0004_auto_20180814_1555'),
    ]

    operations = [
        migrations.AlterField(
            model_name='logentry',
            name='id',
            field=models.BigAutoField(primary_key=True, serialize=False, verbose_name='ID'),
        ),
    ]
