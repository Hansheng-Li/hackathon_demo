# Generated by Django 4.2.7 on 2024-12-31 23:28

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ("hackathon", "0005_alter_projecthackathon_unique_together"),
    ]

    operations = [
        migrations.AddField(
            model_name="project",
            name="created_at",
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]
