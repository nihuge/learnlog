# Generated by Django 2.0 on 2018-04-12 07:26

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('learnlogs', '0004_topic_owner'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='topic',
            name='owner',
        ),
    ]