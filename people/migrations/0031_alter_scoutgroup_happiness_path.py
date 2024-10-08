# Generated by Django 5.0.6 on 2024-07-18 19:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("people", "0030_alter_scoutgroup_happiness_path"),
    ]

    operations = [
        migrations.AlterField(
            model_name="scoutgroup",
            name="happiness_path",
            field=models.CharField(
                blank=True,
                choices=[
                    ("Felici di accogliere", "Felici di accogliere"),
                    ("Felici di vivere una vita giusta", "Felici di vivere una vita giusta"),
                    (
                        "Felici di prendersi cura e custodire",
                        "Felici di prendersi cura e custodire",
                    ),
                    ("Felici di generare speranza", "Felici di generare speranza"),
                    ("Felici di fare esperienza di Dio", "Felici di fare esperienza di Dio"),
                    ("Felici di essere appassionati", "Felici di essere appassionati"),
                    ("Felici di lavorare per la pace", "Felici di lavorare per la pace"),
                    (
                        "Felici di essere profeti in un mondo nuovo",
                        "Felici di essere profeti in un mondo nuovo",
                    ),
                ],
                max_length=255,
                null=True,
                verbose_name="sentiero della felicità",
            ),
        ),
    ]
