# Generated by Django 4.1.1 on 2022-10-10 18:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0002_products_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='products',
            name='public',
            field=models.BooleanField(default=True),
        ),
    ]
