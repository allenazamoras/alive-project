# Generated by Django 2.0.5 on 2018-05-23 04:41

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('userprofile', '0003_auto_20180523_0315'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='reputation',
        ),
    ]
