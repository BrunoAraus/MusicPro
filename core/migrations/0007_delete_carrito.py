# Generated by Django 4.2 on 2023-05-08 22:00

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0006_rename_independencia_producto_dimensiones_and_more'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Carrito',
        ),
    ]
