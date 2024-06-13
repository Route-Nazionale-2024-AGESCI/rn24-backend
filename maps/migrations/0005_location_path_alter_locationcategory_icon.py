# Generated by Django 5.0.6 on 2024-06-13 08:34

import django.contrib.gis.db.models.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("maps", "0004_locationcategory_location_is_public_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="location",
            name="path",
            field=django.contrib.gis.db.models.fields.LineStringField(
                blank=True, null=True, srid=4326, verbose_name="linea"
            ),
        ),
        migrations.AlterField(
            model_name="locationcategory",
            name="icon",
            field=models.CharField(
                blank=True,
                help_text="scegli il codice icona di font awesome https://fontawesome.com/icons",
                max_length=255,
                null=True,
                verbose_name="icona",
            ),
        ),
    ]
