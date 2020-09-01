# Generated by Django 3.1 on 2020-08-31 20:05

import autograder.core.fields
import autograder.core.models.project.project
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0085_honor_pledge_fields'),
    ]

    operations = [
        migrations.AddField(
            model_name='group',
            name='soft_extended_due_date',
            field=models.DateTimeField(blank=True, default=None, help_text='Analogous to Project.soft_closing time, but for\n            extensions. This value will be shown to group members as\n            their new due date, but group members will not be prevented\n            from submitting past this time.\n\n            This field has a few primary use cases:\n                1. Providing a grace period for extension deadlines.\n                2. Granting extensions when a late submission penalty\n                   is also enabled (students have to be able to submit\n                   "after the deadline" for the penalty to be appied.)\n                3. Granting extensions when an early submission bonus\n                   applied in relation to the soft deadline is enabled.', null=True),
        ),
        migrations.AddField(
            model_name='project',
            name='early_submission_bonus',
            field=autograder.core.fields.ValidatedJSONField(default=autograder.core.models.project.project.EarlySubmissionBonus, serializable_class=autograder.core.models.project.project.EarlySubmissionBonus),
        ),
        migrations.AddField(
            model_name='project',
            name='late_submission_penalty',
            field=autograder.core.fields.ValidatedJSONField(default=autograder.core.models.project.project.LateSubmissionPenalty, serializable_class=autograder.core.models.project.project.LateSubmissionPenalty),
        ),
        migrations.AddField(
            model_name='project',
            name='use_early_submission_bonus',
            field=models.BooleanField(default=False, help_text='Whether to apply an early submission bonus to students\'\n            final graded submissions. If this value is true, then\n            ultimate_submission_policy must be "most_recent".\n        '),
        ),
        migrations.AddField(
            model_name='project',
            name='use_late_submission_penalty',
            field=models.BooleanField(default=False, help_text='Whether to apply a late submission penalty to students\'\n            final graded submissions. If this value is true, then\n            ultimate_submission_policy must be "most_recent" and\n            "allow_late_days" must be false.\n        '),
        ),
        migrations.AlterField(
            model_name='group',
            name='extended_due_date',
            field=models.DateTimeField(blank=True, default=None, help_text='When this field is not null, it indicates that members\n            of this submission group can submit until this specified\n            date, overriding the project closing time.\n            Default value: None', null=True),
        ),
    ]