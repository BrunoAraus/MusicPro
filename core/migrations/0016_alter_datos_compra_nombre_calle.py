# Generated by Django 4.2 on 2023-05-15 03:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0015_alter_datos_compra_nombre_calle'),
    ]

    operations = [
        migrations.AlterField(
            model_name='datos_compra',
            name='nombre_calle',
            field=models.CharField(default='N/A', max_length=100, null=True),
        ),
    ]