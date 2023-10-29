# Generated by Django 4.2.6 on 2023-10-27 15:03

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("board", "0001_initial"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="board",
            options={"ordering": ["-created_at"]},
        ),
        migrations.CreateModel(
            name="Nodes",
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
                (
                    "board",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="board.board"
                    ),
                ),
                (
                    "next_player",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="Next Player",
                    ),
                ),
            ],
        ),
    ]
