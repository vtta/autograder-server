# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-07-16 02:00
from __future__ import unicode_literals

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0004_auto_20160716_0159'),
    ]

    operations = [
        migrations.AlterField(
            model_name='project',
            name='num_submissions_per_day',
            field=models.IntegerField(blank=True, default=None, help_text='The number of submissions each group is allowed per\n            day before either reducing feedback or preventing further\n            submissions. A value of None indicates no limit.', null=True, validators=[django.core.validators.MinValueValidator(1)]),
        ),
    ]