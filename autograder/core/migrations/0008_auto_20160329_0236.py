# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-03-29 02:36
from __future__ import unicode_literals

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0007_auto_20160323_0313'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='autogradertestcasebase',
            name='points_for_correct_output',
        ),
        migrations.AddField(
            model_name='autogradertestcasebase',
            name='points_for_correct_stderr',
            field=models.IntegerField(default=0, validators=[django.core.validators.MinValueValidator(0)]),
        ),
        migrations.AddField(
            model_name='autogradertestcasebase',
            name='points_for_correct_stdout',
            field=models.IntegerField(default=0, validators=[django.core.validators.MinValueValidator(0)]),
        ),
    ]