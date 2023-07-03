# Generated by Django 4.2 on 2023-07-03 17:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0018_datos_venta'),
    ]

    operations = [
        migrations.CreateModel(
            name='Peticion',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('nombre_peticion', models.CharField(max_length=100)),
                ('detalle', models.CharField(max_length=300)),
                ('fechas', models.CharField(max_length=100)),
                ('tipo', models.CharField(max_length=100)),
                ('desempeño', models.CharField(default='N/A', max_length=150, null=True)),
                ('cancelaciones', models.IntegerField(default='N/A', null=True)),
                ('total_venta_mes_1', models.IntegerField(default='N/A', null=True)),
                ('total_venta_mes_2', models.IntegerField(default='N/A', null=True)),
                ('productos_vendidos_mes_1', models.IntegerField(default='N/A', null=True)),
                ('productos_vendidos_mes_2', models.IntegerField(default='N/A', null=True)),
                ('estado', models.CharField(default='Pendiente', max_length=100, null=True)),
            ],
        ),
    ]