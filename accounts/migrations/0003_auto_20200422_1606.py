# Generated by Django 2.0.1 on 2020-04-22 10:06

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_auto_20200422_1429'),
    ]

    operations = [
        migrations.RenameField(
            model_name='coursepercentage',
            old_name='course_code',
            new_name='student_course',
        ),
        migrations.RenameField(
            model_name='coursepercentage',
            old_name='session',
            new_name='student_session',
        ),
        migrations.RenameField(
            model_name='coursepercentage',
            old_name='teacher_user',
            new_name='teacher',
        ),
    ]
