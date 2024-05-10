# Generated by Django 5.0.4 on 2024-05-05 10:08

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("maps", "0002_alter_location_polygon"),
        ("people", "0007_populate_subdistrict_district_locations"),
    ]

    operations = [
        migrations.AlterField(
            model_name="district",
            name="location",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                to="maps.location",
                verbose_name="luogo",
            ),
        ),
        migrations.AlterField(
            model_name="subdistrict",
            name="location",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                to="maps.location",
                verbose_name="luogo",
            ),
        ),
    ]