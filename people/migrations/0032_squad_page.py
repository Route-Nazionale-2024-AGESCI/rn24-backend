# Generated by Django 5.0.6 on 2024-07-18 22:40

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("cms", "0003_create_root_pages"),
        ("people", "0031_alter_scoutgroup_happiness_path"),
    ]

    operations = [
        migrations.AddField(
            model_name="squad",
            name="page",
            field=models.ForeignKey(
                blank=True,
                help_text="la pagina CMS viene creata automaticamente al salvataggio dell'evento",
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to="cms.cmspage",
                verbose_name="pagina",
            ),
        ),
    ]
