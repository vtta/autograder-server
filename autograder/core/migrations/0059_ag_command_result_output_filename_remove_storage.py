# Generated by Django 3.0.5 on 2020-04-22 15:40

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0058_auto_20200421_1801'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='agcommandresult',
            name='_stderr_filename',
        ),
        migrations.RemoveField(
            model_name='agcommandresult',
            name='_stdout_filename',
        ),
    ]
