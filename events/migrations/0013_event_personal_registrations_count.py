# Generated by Django 5.0.6 on 2024-06-07 21:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("events", "0012_lineeventregistration_line_event_registered_lines_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="event",
            name="personal_registrations_count",
            field=models.PositiveIntegerField(
                db_index=True, default=0, verbose_name="numero di iscrizioni personali"
            ),
        ),
    ]
