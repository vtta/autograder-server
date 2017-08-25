# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2017-08-25 17:09
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0013_auto_20170825_1604'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='autogradertestcasebase',
            unique_together=set([]),
        ),
        # migrations.RemoveField(
        #     model_name='autogradertestcasebase',
        #     name='feedback_configuration',
        # ),
        # migrations.RemoveField(
        #     model_name='autogradertestcasebase',
        #     name='past_submission_limit_fdbk_conf',
        # ),
        # migrations.RemoveField(
        #     model_name='autogradertestcasebase',
        #     name='polymorphic_ctype',
        # ),
        # migrations.RemoveField(
        #     model_name='autogradertestcasebase',
        #     name='project',
        # ),
        # migrations.RemoveField(
        #     model_name='autogradertestcasebase',
        #     name='project_files_to_compile_together',
        # ),
        # migrations.RemoveField(
        #     model_name='autogradertestcasebase',
        #     name='staff_viewer_fdbk_conf',
        # ),
        # migrations.RemoveField(
        #     model_name='autogradertestcasebase',
        #     name='student_files_to_compile_together',
        # ),
        # migrations.RemoveField(
        #     model_name='autogradertestcasebase',
        #     name='student_resource_files',
        # ),
        # migrations.RemoveField(
        #     model_name='autogradertestcasebase',
        #     name='test_resource_files',
        # ),
        # migrations.RemoveField(
        #     model_name='autogradertestcasebase',
        #     name='ultimate_submission_fdbk_conf',
        # ),
        migrations.AlterUniqueTogether(
            name='autogradertestcaseresult',
            unique_together=set([]),
        ),
        # migrations.RemoveField(
        #     model_name='autogradertestcaseresult',
        #     name='submission',
        # ),
        # migrations.RemoveField(
        #     model_name='autogradertestcaseresult',
        #     name='test_case',
        # ),
        migrations.DeleteModel(
            name='CompilationOnlyAutograderTestCase',
        ),
        migrations.DeleteModel(
            name='CompiledAndRunAutograderTestCase',
        ),
        migrations.DeleteModel(
            name='CompiledAutograderTestCase',
        ),
        migrations.DeleteModel(
            name='InterpretedAutograderTestCase',
        ),
        migrations.DeleteModel(
            name='AutograderTestCaseBase',
        ),
        migrations.DeleteModel(
            name='AutograderTestCaseResult',
        ),
        migrations.DeleteModel(
            name='FeedbackConfig',
        ),
    ]
