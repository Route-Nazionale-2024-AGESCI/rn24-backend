# Generated by Django 5.0.4 on 2024-04-20 17:20

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("cms", "0001_initial"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="cmspage",
            options={"verbose_name": "pagina", "verbose_name_plural": "pagine"},
        ),
    ]