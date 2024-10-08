# Generated by Django 5.0.6 on 2024-05-25 13:38

import django.db.models.manager
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("events", "0009_alter_event_kind"),
    ]

    operations = [
        migrations.AlterModelManagers(
            name="event",
            managers=[
                ("objects_with_annotations", django.db.models.manager.Manager()),
            ],
        ),
        migrations.AlterField(
            model_name="event",
            name="ends_at",
            field=models.DateTimeField(db_index=True, verbose_name="data fine"),
        ),
        migrations.AlterField(
            model_name="event",
            name="is_registration_required",
            field=models.BooleanField(
                db_index=True, default=True, verbose_name="registrazione individuale abilitata?"
            ),
        ),
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
                db_index=True,
                max_length=255,
                verbose_name="modulo",
            ),
        ),
        migrations.AlterField(
            model_name="event",
            name="registration_limit",
            field=models.PositiveIntegerField(
                blank=True, db_index=True, null=True, verbose_name="limite di iscrizioni"
            ),
        ),
        migrations.AlterField(
            model_name="event",
            name="registration_limit_from_same_scout_group",
            field=models.PositiveIntegerField(
                blank=True,
                db_index=True,
                null=True,
                verbose_name="limite di iscrizioni dallo stesso groupo scout",
            ),
        ),
        migrations.AlterField(
            model_name="event",
            name="registrations_close_at",
            field=models.DateTimeField(
                blank=True, db_index=True, null=True, verbose_name="data chiusura iscrizioni"
            ),
        ),
        migrations.AlterField(
            model_name="event",
            name="registrations_open_at",
            field=models.DateTimeField(
                blank=True, db_index=True, null=True, verbose_name="data apertura iscrizioni"
            ),
        ),
        migrations.AlterField(
            model_name="event",
            name="starts_at",
            field=models.DateTimeField(db_index=True, verbose_name="data inizio"),
        ),
    ]
