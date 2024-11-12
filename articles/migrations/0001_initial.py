# Generated by Django 5.1.2 on 2024-11-12 12:16

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Hashtag",
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
                ("name", models.CharField(max_length=50, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name="Article",
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
                    "type",
                    models.CharField(
                        choices=[
                            ("facebook", "Facebook"),
                            ("twitter", "Twitter"),
                            ("instagram", "Instagram"),
                            ("threads", "Threads"),
                        ],
                        default="type",
                        max_length=50,
                    ),
                ),
                ("title", models.CharField(max_length=50)),
                ("content", models.TextField()),
                ("view_count", models.PositiveIntegerField(blank=True, default=0)),
                ("like_count", models.PositiveIntegerField(blank=True, default=0)),
                ("share_count", models.PositiveIntegerField(blank=True, default=0)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                (
                    "likes",
                    models.ManyToManyField(
                        blank=True,
                        related_name="likes_articles",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "hashtags",
                    models.ManyToManyField(
                        blank=True, related_name="articles", to="articles.hashtag"
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="ArticleShare",
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
                    "platform",
                    models.CharField(
                        choices=[
                            ("facebook", "Facebook"),
                            ("twitter", "Twitter"),
                            ("instagram", "Instagram"),
                            ("threads", "Threads"),
                        ],
                        max_length=50,
                    ),
                ),
                ("shared_at", models.DateTimeField(auto_now_add=True)),
                (
                    "article",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="shares",
                        to="articles.article",
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="shared_articles",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
    ]
