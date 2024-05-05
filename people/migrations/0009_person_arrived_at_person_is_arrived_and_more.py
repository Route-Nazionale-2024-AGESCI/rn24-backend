# Generated by Django 5.0.4 on 2024-05-05 11:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("people", "0008_alter_district_location_alter_subdistrict_location"),
    ]

    operations = [
        migrations.AddField(
            model_name="person",
            name="arrived_at",
            field=models.DateTimeField(blank=True, null=True, verbose_name="data di arrivo"),
        ),
        migrations.AddField(
            model_name="person",
            name="is_arrived",
            field=models.BooleanField(default=False, verbose_name="arrivato?"),
        ),
        migrations.AddField(
            model_name="scoutgroup",
            name="is_arrived",
            field=models.BooleanField(default=False, verbose_name="arrivato?"),
        ),
    ]
