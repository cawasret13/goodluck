# Generated by Django 4.1.2 on 2022-11-04 11:28

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='PersonalData',
            fields=[
                ('id', models.CharField(max_length=32, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=256)),
                ('lastname', models.CharField(max_length=256)),
            ],
        ),
    ]
