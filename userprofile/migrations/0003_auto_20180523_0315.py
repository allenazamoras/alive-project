# Generated by Django 2.0.5 on 2018-05-23 03:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('userprofile', '0002_auto_20180523_0252'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='profile_picture',
            field=models.ImageField(default='thumbpath/none/none.jpg', upload_to='thumbpath'),
        ),
    ]
