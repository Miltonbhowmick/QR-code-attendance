# Generated by Django 2.1.4 on 2019-05-17 04:31

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0019_auto_20190517_0130'),
    ]

    operations = [
        migrations.RenameField(
            model_name='studentprofile',
            old_name='image',
            new_name='student_image',
        ),
        migrations.RenameField(
            model_name='studentprofile',
            old_name='session',
            new_name='student_session',
        ),
    ]
