# Generated by Django 5.0.6 on 2024-05-23 21:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("events", "0008_alter_event_kind"),
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
                    ("LOGISTICO", "LOGISTICO"),
                    ("ALTRO", "ALTRO"),
                ],
                max_length=255,
                verbose_name="modulo",
            ),
        ),
    ]
