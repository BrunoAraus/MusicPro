# Generated by Django 4.2 on 2023-05-15 03:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0013_alter_datos_compra_nombre_calle_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='datos_compra',
            name='numero_calle',
            field=models.IntegerField(default=0, null=True),
        ),
        migrations.AlterField(
            model_name='datos_compra',
            name='region',
            field=models.CharField(max_length=50, null=True),
        ),
    ]
