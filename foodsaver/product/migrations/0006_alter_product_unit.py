# Generated by Django 4.1.3 on 2022-11-28 17:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("product", "0005_product_unit_alter_product_name"),
    ]

    operations = [
        migrations.AlterField(
            model_name="product",
            name="unit",
            field=models.CharField(max_length=255),
        ),
    ]