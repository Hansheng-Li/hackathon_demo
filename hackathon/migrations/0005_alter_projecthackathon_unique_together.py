# Generated by Django 4.2.7 on 2024-12-31 20:07

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("hackathon", "0004_projecthackathon_project_hackathons"),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name="projecthackathon",
            unique_together={("project", "hackathon")},
        ),
    ]
