# Generated by Django 5.1 on 2024-08-23 17:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cloth_product', '0003_review'),
    ]

    operations = [
        migrations.AlterField(
            model_name='review',
            name='image',
            field=models.ImageField(upload_to='cloth_product/media2/images'),
        ),
    ]