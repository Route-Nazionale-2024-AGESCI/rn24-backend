# Generated by Django 5.1 on 2024-08-24 14:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("people", "0041_line_square_meters_line_tent_slots"),
    ]

    operations = [
        migrations.AlterField(
            model_name="scoutgroup",
            name="is_arrived",
            field=models.BooleanField(
                db_index=True, default=False, verbose_name="almeno un presente?"
            ),
        ),
    ]
