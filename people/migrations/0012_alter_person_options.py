# Generated by Django 5.0.4 on 2024-05-05 14:35

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("people", "0011_squad_groups"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="person",
            options={
                "permissions": (("is_staff", "Può accedere al backoffice"),),
                "verbose_name": "persona",
                "verbose_name_plural": "persone",
            },
        ),
    ]