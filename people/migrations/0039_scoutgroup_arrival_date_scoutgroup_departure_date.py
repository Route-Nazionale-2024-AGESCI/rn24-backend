# Generated by Django 5.1 on 2024-08-19 13:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("people", "0038_alter_district_location"),
    ]

    operations = [
        migrations.AddField(
            model_name="scoutgroup",
            name="arrival_date",
            field=models.DateTimeField(blank=True, null=True, verbose_name="data di arrivo"),
        ),
        migrations.AddField(
            model_name="scoutgroup",
            name="departure_date",
            field=models.DateTimeField(blank=True, null=True, verbose_name="data di partenza"),
        ),
    ]