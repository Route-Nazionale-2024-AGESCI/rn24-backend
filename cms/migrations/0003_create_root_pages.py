# Generated by Django 5.0.4 on 2024-04-20 18:14

from django.core.management import call_command
from django.db import migrations


def create_root_pages(apps, schema_editor):
    call_command("create_root_pages")


class Migration(migrations.Migration):

    dependencies = [
        ("cms", "0002_alter_cmspage_options"),
    ]

    operations = [
        migrations.RunPython(create_root_pages, migrations.RunPython.noop),
    ]
