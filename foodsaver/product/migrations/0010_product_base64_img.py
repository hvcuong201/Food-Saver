# Generated by Django 4.1.3 on 2022-12-01 06:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("product", "0009_alter_product_category"),
    ]

    operations = [
        migrations.AddField(
            model_name="product",
            name="base64_img",
            field=models.CharField(max_length=255, null=True),
        ),
    ]