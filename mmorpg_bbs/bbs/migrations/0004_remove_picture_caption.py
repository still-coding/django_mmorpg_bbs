# Generated by Django 4.2.5 on 2023-09-20 19:29

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("bbs", "0003_picture"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="picture",
            name="caption",
        ),
    ]