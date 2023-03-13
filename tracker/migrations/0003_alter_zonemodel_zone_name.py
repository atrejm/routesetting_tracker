# Generated by Django 4.1 on 2023-03-12 20:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("tracker", "0002_alter_zonemodel_zone_name"),
    ]

    operations = [
        migrations.AlterField(
            model_name="zonemodel",
            name="zone_name",
            field=models.CharField(
                choices=[
                    ("Zone 1", "Zone 1"),
                    ("Zone 2", "Zone 2"),
                    ("Zone 3", "Zone 3"),
                    ("Zone 4", "Zone 4"),
                    ("Zone 5", "Zone 5"),
                    ("Zone 6", "Zone 6"),
                    ("Zone 7", "Zone 7"),
                    ("Zone 8", "Zone 8"),
                    ("Zone 9", "Zone 9"),
                    ("Zone 10", "Zone 10"),
                    ("Zone 11", "Zone 11"),
                    ("Zone 12", "Zone 12"),
                    ("Zone 13", "Zone 13"),
                    ("Zone 14", "Zone 14"),
                    ("Zone 15", "Zone 15"),
                    ("Zone 16", "Zone 16"),
                ],
                max_length=20,
            ),
        ),
    ]
