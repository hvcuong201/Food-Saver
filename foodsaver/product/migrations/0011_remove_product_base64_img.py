# Generated by Django 4.1.3 on 2022-12-01 07:03

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("product", "0010_product_base64_img"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="product",
            name="base64_img",
        ),
    ]