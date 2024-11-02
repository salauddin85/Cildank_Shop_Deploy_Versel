# Generated by Django 5.1.2 on 2024-10-31 20:02

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cloth_product', '0016_remove_coustomerwishlistproduct_user_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='coustomerwishlistproduct',
            name='wishlist',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='wishlist_products', to='cloth_product.wishlist'),
        ),
    ]
