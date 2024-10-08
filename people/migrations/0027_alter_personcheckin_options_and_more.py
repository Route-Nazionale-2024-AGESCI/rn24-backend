# Generated by Django 5.0.6 on 2024-07-17 22:05

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("people", "0026_personcheckin"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="personcheckin",
            options={"verbose_name": "entrata - uscita", "verbose_name_plural": "entrate - uscite"},
        ),
        migrations.AddField(
            model_name="person",
            name="identity_document_expiry_date",
            field=models.DateField(blank=True, null=True, verbose_name="data scadenza documento"),
        ),
        migrations.AddField(
            model_name="person",
            name="identity_document_issue_date",
            field=models.DateField(blank=True, null=True, verbose_name="data rilascio documento"),
        ),
        migrations.AddField(
            model_name="person",
            name="identity_document_number",
            field=models.CharField(
                blank=True, max_length=255, null=True, verbose_name="numero documento"
            ),
        ),
        migrations.AddField(
            model_name="person",
            name="identity_document_type",
            field=models.CharField(
                blank=True, max_length=255, null=True, verbose_name="tipo documento"
            ),
        ),
        migrations.AlterField(
            model_name="person",
            name="accessibility_has_caretaker_not_registered",
            field=models.BooleanField(
                db_index=True,
                default=False,
                help_text="viaggia con accompagnatore non iscritto?",
                verbose_name="accompagnatore?",
            ),
        ),
        migrations.AlterField(
            model_name="person",
            name="accessibility_has_wheelchair",
            field=models.BooleanField(
                db_index=True, default=False, verbose_name="sedia a rotelle?"
            ),
        ),
        migrations.AlterField(
            model_name="person",
            name="food_diet_needed",
            field=models.CharField(
                blank=True,
                choices=[
                    ("Nessuna", "Nessuna"),
                    (
                        "Monodieta (selezionare nel caso di singola allergia/intolleranza)",
                        "Monodieta (selezionare nel caso di singola allergia/intolleranza)",
                    ),
                    (
                        "Multidieta (selezionare nel caso di più allergie/intolleranze)",
                        "Multidieta (selezionare nel caso di più allergie/intolleranze)",
                    ),
                    (
                        "Dieta da shock (selezionare nel caso di una o più allergie che possano causare shock anafilattico)",
                        "Dieta da shock (selezionare nel caso di una o più allergie che possano causare shock anafilattico)",
                    ),
                ],
                db_index=True,
                help_text="Allergie/intolleranze ad alimenti da segnalare.",
                max_length=255,
                null=True,
                verbose_name="dieta",
            ),
        ),
        migrations.AlterField(
            model_name="person",
            name="food_is_vegan",
            field=models.BooleanField(
                db_index=True,
                default=False,
                help_text="Segui una dieta vegana?",
                verbose_name="vegano?",
            ),
        ),
        migrations.AlterField(
            model_name="person",
            name="health_has_allergies",
            field=models.BooleanField(
                db_index=True,
                default=False,
                help_text="Hai allergie accertate?",
                verbose_name="allergie?",
            ),
        ),
        migrations.AlterField(
            model_name="person",
            name="health_has_movement_disorders",
            field=models.BooleanField(
                db_index=True,
                default=False,
                help_text="Sei affetto da disturbi motori?",
                verbose_name="disturbi motori?",
            ),
        ),
        migrations.AlterField(
            model_name="person",
            name="health_has_patologies",
            field=models.BooleanField(
                db_index=True,
                default=False,
                help_text="Sei affetto da patologie cardiovascolari/respiratorie/neurologiche?",
                verbose_name="patologie?",
            ),
        ),
        migrations.AlterField(
            model_name="person",
            name="sleeping_is_sleeping_in_tent",
            field=models.BooleanField(
                db_index=True,
                default=False,
                help_text="dorme in tenda personale?",
                verbose_name="tenda?",
            ),
        ),
        migrations.AlterField(
            model_name="person",
            name="transportation_has_problems_moving_on_foot",
            field=models.BooleanField(
                db_index=True,
                default=False,
                help_text="Hai disabilità/patologie/età che non ti permettono di sostenere gli spostamenti a piedi previsti?",
                verbose_name="spostamento a piedi?",
            ),
        ),
        migrations.AlterField(
            model_name="personcheckin",
            name="direction",
            field=models.CharField(
                choices=[("ENTRATA", "ENTRATA"), ("USCITA", "USCITA")],
                db_index=True,
                max_length=255,
                verbose_name="direzione",
            ),
        ),
        migrations.AlterField(
            model_name="personcheckin",
            name="user",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                to=settings.AUTH_USER_MODEL,
                verbose_name="utente",
            ),
        ),
    ]
