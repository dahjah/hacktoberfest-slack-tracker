# Generated by Django 3.1.2 on 2020-10-05 18:53

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('github_checker', '0004_auto_20201005_1823'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='NotificationSettings',
            new_name='NotificationSetting',
        ),
        migrations.RenameField(
            model_name='connectionuserconfig',
            old_name='email',
            new_name='slack_name',
        ),
    ]
