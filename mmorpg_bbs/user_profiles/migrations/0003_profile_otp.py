# Generated by Django 4.2.5 on 2023-09-20 10:13

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("user_profiles", "0002_profile_mailing_period"),
    ]

    operations = [
        migrations.AddField(
            model_name="profile",
            name="otp",
            field=models.IntegerField(default=0),
        ),
    ]
