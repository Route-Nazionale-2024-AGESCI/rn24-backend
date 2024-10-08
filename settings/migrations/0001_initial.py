# Generated by Django 5.0.6 on 2024-07-10 19:49

import django.db.models.manager
import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Setting",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True, primary_key=True, serialize=False, verbose_name="ID"
                    ),
                ),
                (
                    "created_at",
                    models.DateTimeField(
                        auto_now_add=True, db_index=True, verbose_name="data di creazione"
                    ),
                ),
                (
                    "updated_at",
                    models.DateTimeField(
                        auto_now=True, db_index=True, verbose_name="data ultima modifica"
                    ),
                ),
                (
                    "uuid",
                    models.UUIDField(
                        db_index=True,
                        default=uuid.uuid4,
                        editable=False,
                        unique=True,
                        verbose_name="UUID",
                    ),
                ),
                (
                    "deleted_at",
                    models.DateTimeField(
                        blank=True,
                        db_index=True,
                        editable=False,
                        null=True,
                        verbose_name="data di cancellazione",
                    ),
                ),
                ("key", models.CharField(max_length=255, unique=True)),
                ("value", models.CharField(blank=True, max_length=255, null=True)),
            ],
            options={
                "verbose_name": "impostazione",
                "verbose_name_plural": "impostazioni",
            },
            managers=[
                ("objects_with_deleted", django.db.models.manager.Manager()),
            ],
        ),
    ]
