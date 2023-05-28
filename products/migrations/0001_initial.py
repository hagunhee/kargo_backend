# Generated by Django 4.1.6 on 2023-05-26 07:02

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Product",
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
                ("name", models.CharField(max_length=255)),
                ("original_price", models.PositiveIntegerField()),
                ("stock_quantity", models.PositiveIntegerField()),
                ("description", models.TextField(blank=True)),
                ("imageURL", models.ImageField(blank=True, upload_to="product_images")),
                ("is_deleted", models.BooleanField(default=False)),
                ("commission", models.PositiveIntegerField(default=0)),
            ],
            options={
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="ProductPost",
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
                ("name", models.CharField(default="", max_length=255)),
                ("price_for_1", models.PositiveIntegerField(blank=True, null=True)),
                ("price_for_2", models.PositiveIntegerField(blank=True, null=True)),
                ("price_for_10", models.PositiveIntegerField(blank=True, null=True)),
                ("price_for_50", models.PositiveIntegerField(blank=True, null=True)),
                ("visibility", models.BooleanField(default=False)),
                ("publish_time", models.DateTimeField()),
                ("onsale", models.BooleanField(default=False)),
                ("event_start_date", models.DateTimeField(blank=True, null=True)),
                ("event_end_date", models.DateTimeField(blank=True, null=True)),
                ("event_discount", models.PositiveIntegerField(blank=True, null=True)),
                ("is_deleted", models.BooleanField(default=False)),
                (
                    "product",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="product_posts",
                        to="products.product",
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
    ]
