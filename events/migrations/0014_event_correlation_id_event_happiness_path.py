# Generated by Django 5.0.6 on 2024-06-13 10:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("events", "0013_event_personal_registrations_count"),
    ]

    operations = [
        migrations.AddField(
            model_name="event",
            name="correlation_id",
            field=models.CharField(
                blank=True,
                db_index=True,
                help_text="deve essere uguale per tutti gli accandimenti dello stesso evento",
                max_length=255,
                null=True,
                verbose_name="id di correlazione accadimenti",
            ),
        ),
        migrations.AddField(
            model_name="event",
            name="happiness_path",
            field=models.CharField(
                blank=True,
                choices=[
                    ("FELICI_DI_ACCOGLIERE", "Felici di accogliere"),
                    ("FELICI_DI_VIVERE_UNA_VITA_GIUSTA", "Felici di vivere una vita giusta"),
                    (
                        "FELICI_DI_PRENDERSI_CURA_E_CUSTODIRE",
                        "Felici di prendersi cura e custodire",
                    ),
                    ("FELICI_DI_GENERARE_SPERANZA", "Felici di generare speranza"),
                    ("FELICI_DI_FARE_ESPERIENZA_DI_DIO", "Felici di fare esperienza di Dio"),
                    ("FELICI_DI_ESSERE_APPASSIONATI", "Felici di essere appassionati"),
                    ("FELICI_DI_LAVORARE_PER_LA_PACE", "Felici di lavorare per la pace"),
                    (
                        "FELICI_DI_ESSERE_PROFETI_IN_UN_MONDO_NUOVO",
                        "Felici di essere profeti in un mondo nuovo",
                    ),
                ],
                max_length=255,
                null=True,
                verbose_name="sentiero della felicità",
            ),
        ),
    ]
