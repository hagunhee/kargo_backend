# Generated by Django 4.1.6 on 2023-06-19 21:36

from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Coupon",
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
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                (
                    "name",
                    models.CharField(blank=True, default="", max_length=255, null=True),
                ),
                (
                    "role",
                    models.CharField(
                        choices=[
                            ("all", "All Items"),
                            ("brand", "Specific Brands"),
                            ("product", "Specific ProductPosts"),
                            ("category", "Specific Category"),
                            ("influencer", "Specific Influencer"),
                            ("group", "Specific Group"),
                        ],
                        default="all",
                        max_length=50,
                    ),
                ),
                (
                    "code",
                    models.CharField(
                        blank=True, max_length=100, null=True, unique=True
                    ),
                ),
                ("discount_amount", models.PositiveIntegerField(default=0)),
                ("is_used", models.BooleanField(default=False)),
                ("used_at", models.DateTimeField(blank=True, null=True)),
                ("expired_at", models.DateTimeField(blank=True, null=True)),
            ],
            options={
                "abstract": False,
            },
        ),
    ]
