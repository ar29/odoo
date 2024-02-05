# Generated by Django 4.2.9 on 2024-02-04 12:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('room_booking', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='access_token',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='phone_number',
            field=models.CharField(max_length=15, unique=True),
        ),
    ]
