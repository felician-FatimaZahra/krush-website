# Generated by Django 3.0.7 on 2020-07-02 00:50

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_friend_current_user'),
    ]

    operations = [
        migrations.RenameField(
            model_name='friend',
            old_name='current_user',
            new_name='from_user',
        ),
        migrations.RenameField(
            model_name='friend',
            old_name='users',
            new_name='to_user',
        ),
    ]
