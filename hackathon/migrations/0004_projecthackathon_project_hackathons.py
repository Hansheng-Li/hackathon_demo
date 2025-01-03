# Generated by Django 4.2.7 on 2024-12-31 19:53

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ("hackathon", "0003_remove_project_hackathons"),
    ]

    operations = [
        migrations.CreateModel(
            name="ProjectHackathon",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("apply_time", models.DateTimeField(default=django.utils.timezone.now)),
                (
                    "hackathon",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="hackathon.hackathon",
                    ),
                ),
                (
                    "project",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="hackathon.project",
                    ),
                ),
            ],
        ),
        migrations.AddField(
            model_name="project",
            name="hackathons",
            field=models.ManyToManyField(
                blank=True,
                related_name="projects",
                through="hackathon.ProjectHackathon",
                to="hackathon.hackathon",
            ),
        ),
    ]
