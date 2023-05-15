# Generated by Django 4.2 on 2023-05-15 03:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0012_remove_datos_compra_despacho_datos_compra_region_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='datos_compra',
            name='nombre_calle',
            field=models.CharField(default='N/A', max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='datos_compra',
            name='numero_calle',
            field=models.IntegerField(default='N/A', null=True),
        ),
        migrations.AlterField(
            model_name='datos_compra',
            name='region',
            field=models.CharField(default='N/A', max_length=50, null=True),
        ),
    ]