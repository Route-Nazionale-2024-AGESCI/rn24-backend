# Generated by Django 5.0.6 on 2024-05-18 13:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("maps", "0002_alter_location_polygon"),
    ]

    operations = [
        migrations.AlterField(
            model_name="location",
            name="name",
            field=models.CharField(db_index=True, max_length=255, verbose_name="nome"),
        ),
    ]
