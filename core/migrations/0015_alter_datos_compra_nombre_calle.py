# Generated by Django 4.2 on 2023-05-15 03:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0014_alter_datos_compra_numero_calle_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='datos_compra',
            name='nombre_calle',
            field=models.CharField(default='', max_length=100, null=True),
        ),
    ]