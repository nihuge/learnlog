# Generated by Django 2.0 on 2018-04-17 02:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('learnlogs', '0006_topic_owner'),
    ]

    operations = [
        migrations.AddField(
            model_name='entry',
            name='title',
            field=models.CharField(default=1, max_length=255),
            preserve_default=False,
        ),
    ]