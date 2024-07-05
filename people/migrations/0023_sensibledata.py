# Generated by Django 5.0.6 on 2024-07-05 14:26

import django.db.models.manager
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("people", "0022_alter_person_region_and_more"),
    ]

    operations = [
        migrations.CreateModel(
            name="SensibleData",
            fields=[],
            options={
                "verbose_name": "Dati sensibili",
                "verbose_name_plural": "Dati sensibili",
                "proxy": True,
                "indexes": [],
                "constraints": [],
            },
            bases=("people.person",),
            managers=[
                ("objects_with_deleted", django.db.models.manager.Manager()),
            ],
        ),
    ]
