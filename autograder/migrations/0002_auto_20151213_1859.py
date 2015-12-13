# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2015-12-13 18:59
from __future__ import unicode_literals

import autograder.fields
import autograder.shared.feedback_configuration
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('autograder', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='studenttestsuitebase',
            name='feedback_configuration',
            field=autograder.fields.JsonSerializableClassField(class_=autograder.shared.feedback_configuration.StudentTestSuiteFeedbackConfiguration, default=autograder.shared.feedback_configuration.StudentTestSuiteFeedbackConfiguration),
        ),
        migrations.AlterField(
            model_name='autogradertestcasebase',
            name='compiler',
            field=models.CharField(blank=True, choices=[('g++', 'g++')], max_length=255),
        ),
    ]