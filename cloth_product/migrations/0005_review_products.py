# Generated by Django 5.1 on 2024-08-24 16:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cloth_product', '0004_alter_review_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='review',
            name='products',
            field=models.ManyToManyField(blank=True, null=True, to='cloth_product.product'),
        ),
    ]