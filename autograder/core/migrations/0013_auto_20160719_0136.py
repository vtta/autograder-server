# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-07-19 01:36
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0012_auto_20160719_0132'),
    ]

    operations = [
        migrations.AlterField(
            model_name='autogradertestcasebase',
            name='feedback_configuration',
            field=models.OneToOneField(blank=True, help_text='Specifies how much information should be included\n            in serialized run results. If not specified on creation,\n            this field is initialized to a default-constructed\n            FeedbackConfig object.', on_delete=django.db.models.deletion.CASCADE, related_name='ag_test', to='core.FeedbackConfig'),
        ),
    ]