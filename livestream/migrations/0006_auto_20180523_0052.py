# Generated by Django 2.0.5 on 2018-05-23 00:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('livestream', '0005_approvalrequest'),
    ]

    operations = [
        migrations.AlterField(
            model_name='appeal',
            name='is_active',
            field=models.NullBooleanField(),
        ),
    ]
