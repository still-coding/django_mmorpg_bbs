# Generated by Django 4.2.5 on 2023-09-20 17:48

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("bbs", "0002_delete_profile"),
    ]

    operations = [
        migrations.CreateModel(
            name="Picture",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("image", models.ImageField(upload_to="ads_pictures")),
                ("caption", models.CharField(max_length=255)),
                (
                    "ad",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="bbs.ad"
                    ),
                ),
            ],
        ),
    ]
