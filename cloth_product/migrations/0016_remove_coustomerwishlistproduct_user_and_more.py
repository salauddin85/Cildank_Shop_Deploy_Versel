# Generated by Django 5.1.2 on 2024-10-31 19:31

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cloth_product', '0015_coustomerwishlistproduct_user'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='coustomerwishlistproduct',
            name='user',
        ),
        migrations.RemoveField(
            model_name='wishlist',
            name='products',
        ),
    ]