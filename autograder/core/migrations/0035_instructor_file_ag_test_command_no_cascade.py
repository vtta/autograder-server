# Generated by Django 2.0.1 on 2019-02-09 19:53

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0034_course_allowed_guest_domain'),
    ]

    operations = [
        migrations.AlterField(
            model_name='agtestcommand',
            name='expected_stderr_instructor_file',
            field=models.ForeignKey(blank=True, default=None, help_text="An InstructorFile whose contents should be compared against this command's\n                     stderr. This value is used (and may not be null) when expected_stderr_source\n                     is ExpectedOutputSource.instructor_file and is ignored otherwise.", null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='core.InstructorFile'),
        ),
        migrations.AlterField(
            model_name='agtestcommand',
            name='expected_stdout_instructor_file',
            field=models.ForeignKey(blank=True, default=None, help_text="An InstructorFile whose contents should be compared against this command's\n                     stdout. This value is used (and may not be null) when expected_stdout_source\n                     is ExpectedOutputSource.instructor_file and is ignored otherwise.", null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='core.InstructorFile'),
        ),
        migrations.AlterField(
            model_name='agtestcommand',
            name='stdin_instructor_file',
            field=models.ForeignKey(blank=True, default=None, help_text='An InstructorFile whose contents should be redirected to the stdin of this\n                     command. This value is used when stdin_source is StdinSource.instructor_file\n                     and is ignored otherwise.', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='core.InstructorFile'),
        ),
    ]