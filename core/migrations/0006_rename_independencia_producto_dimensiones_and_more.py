# Generated by Django 4.2 on 2023-05-08 20:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0005_alter_producto_descripcion'),
    ]

    operations = [
        migrations.RenameField(
            model_name='producto',
            old_name='independencia',
            new_name='dimensiones',
        ),
        migrations.AddField(
            model_name='producto',
            name='imagen4',
            field=models.CharField(blank=True, max_length=400),
        ),
        migrations.AddField(
            model_name='producto',
            name='impedancia',
            field=models.CharField(blank=True, default='N/A', max_length=400),
        ),
        migrations.AddField(
            model_name='producto',
            name='potencia',
            field=models.CharField(blank=True, default='N/A', max_length=400),
        ),
        migrations.AlterField(
            model_name='producto',
            name='descripcion',
            field=models.CharField(max_length=5000),
        ),
        migrations.AlterField(
            model_name='producto',
            name='peso',
            field=models.CharField(blank=True, default='N/A', max_length=400),
        ),
    ]