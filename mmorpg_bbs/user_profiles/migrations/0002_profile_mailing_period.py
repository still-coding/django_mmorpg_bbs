# Generated by Django 4.2.5 on 2023-09-20 06:10

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("user_profiles", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="profile",
            name="mailing_period",
            field=models.IntegerField(default=0),
        ),
    ]
