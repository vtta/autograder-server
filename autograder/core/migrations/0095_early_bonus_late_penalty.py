# Generated by Django 2.2.18 on 2021-03-01 18:19

import autograder.core.fields
import autograder.core.models.project.project
import django.contrib.postgres.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0094_group_allow_submissions_past_extension'),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='early_submission_bonuses',
            field=django.contrib.postgres.fields.ArrayField(base_field=autograder.core.fields.ValidatedJSONField(serializable_class=autograder.core.models.project.project.EarlySubmissionBonus), blank=True, default=list, help_text="A list of objects describing this project's early\n            submission bonus policy. The bonuses computed from this list\n            are applied additively, i.e., if there is one entry that grants\n            a 5% bonus for being 4 hours early and another that grants a 3%\n            bonus for being 8 hours early, a submission that is 8 hours early\n            will receive an 8% bonus.\n        ", size=None),
        ),
        migrations.AddField(
            model_name='project',
            name='late_submission_penalties',
            field=django.contrib.postgres.fields.ArrayField(base_field=autograder.core.fields.ValidatedJSONField(serializable_class=autograder.core.models.project.project.LateSubmissionPenalty), blank=True, default=list, help_text="A list of objects describing this project's late\n            submission penalty policy. The penalties computed from this list\n            are applied additively, i.e., if there is one entry that applies\n            a 5% penalty for being 4 hours late and another that applies a 3%\n            penalty for being 8 hours late, a submission that is 8 hours late\n            will receive an 8% penalty.\n        ", size=None),
        ),
    ]
