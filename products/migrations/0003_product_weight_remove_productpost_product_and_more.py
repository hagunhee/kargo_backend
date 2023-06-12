# Generated by Django 4.1.6 on 2023-05-29 20:59

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("products", "0002_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="product",
            name="weight",
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.RemoveField(
            model_name="productpost",
            name="product",
        ),
        migrations.AddField(
            model_name="productpost",
            name="product",
            field=models.ManyToManyField(
                related_name="product_posts", to="products.product"
            ),
        ),
    ]
