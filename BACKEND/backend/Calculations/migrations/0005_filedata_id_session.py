# Generated by Django 4.1.2 on 2022-10-26 17:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Calculations', '0004_rename_puth_filedata_path'),
    ]

    operations = [
        migrations.AddField(
            model_name='filedata',
            name='id_session',
            field=models.IntegerField(null=True),
        ),
    ]
