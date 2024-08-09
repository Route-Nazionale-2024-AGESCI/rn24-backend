# Generated by Django 5.1 on 2024-08-09 15:23

import django.contrib.gis.db.models.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("maps", "0007_location_description"),
    ]

    operations = [
        migrations.AlterField(
            model_name="location",
            name="coords",
            field=django.contrib.gis.db.models.fields.PointField(
                blank=True, null=True, srid=4326, verbose_name="coordinate"
            ),
        ),
    ]
