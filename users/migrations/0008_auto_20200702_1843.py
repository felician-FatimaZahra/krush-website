# Generated by Django 3.0.7 on 2020-07-02 18:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0007_auto_20200702_1722'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='slug',
            field=models.SlugField(max_length=100),
        ),
    ]
