# Generated by Django 5.0.6 on 2024-07-08 20:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("people", "0023_sensibledata"),
    ]

    operations = [
        migrations.AddField(
            model_name="person",
            name="notes",
            field=models.TextField(blank=True, null=True, verbose_name="note"),
        ),
    ]