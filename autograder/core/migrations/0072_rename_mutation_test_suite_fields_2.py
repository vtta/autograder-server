# Generated by Django 3.0.5 on 2020-05-05 14:37

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0071_rename_mutation_test_suite_fields'),
    ]

    operations = [
        migrations.RenameField(
            model_name='rerunsubmissionstask',
            old_name='student_suite_pks',
            new_name='mutation_suite_pks',
        ),
        migrations.RenameField(
            model_name='rerunsubmissionstask',
            old_name='rerun_all_student_test_suites',
            new_name='rerun_all_mutation_test_suites',
        ),
    ]
