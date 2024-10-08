# Generated by Django 5.0.3 on 2024-04-05 21:21

import django.db.models.deletion
import django.db.models.manager
import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("events", "0003_districteventvisibility_and_more"),
        ("people", "0003_alter_person_user_alter_scoutgroup_region"),
    ]

    operations = [
        migrations.AlterField(
            model_name="event",
            name="visibility_to_districts",
            field=models.ManyToManyField(
                related_name="visible_events",
                through="events.DistrictEventVisibility",
                to="people.district",
            ),
        ),
        migrations.AlterField(
            model_name="event",
            name="visibility_to_persons",
            field=models.ManyToManyField(
                related_name="visible_events",
                through="events.PersonEventVisibility",
                to="people.person",
            ),
        ),
        migrations.AlterField(
            model_name="event",
            name="visibility_to_scout_groups",
            field=models.ManyToManyField(
                related_name="visible_events",
                through="events.ScoutGroupEventVisibility",
                to="people.scoutgroup",
            ),
        ),
        migrations.AlterField(
            model_name="event",
            name="visibility_to_squads",
            field=models.ManyToManyField(
                related_name="visible_events",
                through="events.SquadEventVisibility",
                to="people.squad",
            ),
        ),
        migrations.AlterField(
            model_name="event",
            name="visibility_to_subdistricts",
            field=models.ManyToManyField(
                related_name="visible_events",
                through="events.SubdistrictEventVisibility",
                to="people.subdistrict",
            ),
        ),
        migrations.CreateModel(
            name="DistrictEventRegistration",
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
                (
                    "district",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="people.district",
                        verbose_name="sottocampo",
                    ),
                ),
                (
                    "event",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="events.event",
                        verbose_name="evento",
                    ),
                ),
            ],
            options={
                "verbose_name": "registrazione evento a sottocampo",
                "verbose_name_plural": "registrazione evento a sottocampo",
            },
            managers=[
                ("objects_with_deleted", django.db.models.manager.Manager()),
            ],
        ),
        migrations.AddField(
            model_name="event",
            name="registered_districts",
            field=models.ManyToManyField(
                related_name="registered_events",
                through="events.DistrictEventRegistration",
                to="people.district",
            ),
        ),
        migrations.CreateModel(
            name="PersonEventRegistration",
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
                (
                    "event",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="events.event",
                        verbose_name="evento",
                    ),
                ),
                (
                    "person",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="people.person",
                        verbose_name="persona",
                    ),
                ),
            ],
            options={
                "verbose_name": "registrazione evento a persona",
                "verbose_name_plural": "registrazione evento a persona",
            },
            managers=[
                ("objects_with_deleted", django.db.models.manager.Manager()),
            ],
        ),
        migrations.AddField(
            model_name="event",
            name="registered_persons",
            field=models.ManyToManyField(
                related_name="registered_events",
                through="events.PersonEventRegistration",
                to="people.person",
            ),
        ),
        migrations.CreateModel(
            name="ScoutGroupEventRegistration",
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
                (
                    "event",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="events.event",
                        verbose_name="evento",
                    ),
                ),
                (
                    "scout_group",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="people.scoutgroup",
                        verbose_name="gruppo scout",
                    ),
                ),
            ],
            options={
                "verbose_name": "registrazione evento a gruppo scout",
                "verbose_name_plural": "registrazione evento a gruppo scout",
            },
            managers=[
                ("objects_with_deleted", django.db.models.manager.Manager()),
            ],
        ),
        migrations.AddField(
            model_name="event",
            name="registered_scout_groups",
            field=models.ManyToManyField(
                related_name="registered_events",
                through="events.ScoutGroupEventRegistration",
                to="people.scoutgroup",
            ),
        ),
        migrations.CreateModel(
            name="SquadEventRegistration",
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
                (
                    "event",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="events.event",
                        verbose_name="evento",
                    ),
                ),
                (
                    "squad",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="people.squad",
                        verbose_name="pattuglia",
                    ),
                ),
            ],
            options={
                "verbose_name": "registrazione evento a pattuglia",
                "verbose_name_plural": "registrazione evento a pattuglia",
            },
            managers=[
                ("objects_with_deleted", django.db.models.manager.Manager()),
            ],
        ),
        migrations.AddField(
            model_name="event",
            name="registered_squads",
            field=models.ManyToManyField(
                related_name="registered_events",
                through="events.SquadEventRegistration",
                to="people.squad",
            ),
        ),
        migrations.CreateModel(
            name="SubdistrictEventRegistration",
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
                (
                    "event",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="events.event",
                        verbose_name="evento",
                    ),
                ),
                (
                    "subdistrict",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="people.subdistrict",
                        verbose_name="contrada",
                    ),
                ),
            ],
            options={
                "verbose_name": "registrazione evento a contrada",
                "verbose_name_plural": "registrazione evento a contrada",
            },
            managers=[
                ("objects_with_deleted", django.db.models.manager.Manager()),
            ],
        ),
        migrations.AddField(
            model_name="event",
            name="registered_subdistricts",
            field=models.ManyToManyField(
                related_name="registered_events",
                through="events.SubdistrictEventRegistration",
                to="people.subdistrict",
            ),
        ),
    ]
