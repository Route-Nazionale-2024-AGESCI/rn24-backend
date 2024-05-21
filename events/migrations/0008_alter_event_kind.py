# Generated by Django 5.0.6 on 2024-05-18 13:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("events", "0007_alter_event_kind_alter_event_page"),
    ]

    operations = [
        migrations.AlterField(
            model_name="event",
            name="kind",
            field=models.CharField(
                choices=[
                    ("SGUARDI", "SGUARDI"),
                    ("INCONTRI", "INCONTRI"),
                    ("TRACCE", "TRACCE"),
                    ("CONFRONTI", "CONFRONTI"),
                    ("PASTI", "PASTI"),
                    ("DOCCIA", "DOCCIA"),
                    ("ALTRO", "ALTRO"),
                ],
                max_length=255,
                verbose_name="modulo",
            ),
        ),
    ]