<<<<<<< HEAD
# Generated by Django 4.2 on 2023-05-12 00:31
=======
# Generated by Django 4.2 on 2023-05-12 00:38
>>>>>>> 73e2e9789a7c5198cbbd8c85c07018782f195925

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0007_delete_carrito'),
    ]

    operations = [
        migrations.RenameField(
            model_name='producto',
            old_name='diametro',
            new_name='altavoz',
        ),
        migrations.RenameField(
            model_name='producto',
            old_name='impedancia',
            new_name='cuerpo',
        ),
        migrations.RenameField(
            model_name='producto',
            old_name='respuesta',
            new_name='otros',
        ),
        migrations.AddField(
            model_name='producto',
            name='descripcion_p2',
            field=models.CharField(max_length=5000, null=True),
        ),
        migrations.AddField(
            model_name='producto',
            name='descripcion_p3',
            field=models.CharField(max_length=5000, null=True),
        ),
        migrations.AddField(
            model_name='producto',
            name='descripcion_p4',
            field=models.CharField(max_length=5000, null=True),
        ),
        migrations.AddField(
            model_name='producto',
            name='pastillas',
            field=models.CharField(blank=True, default='N/A', max_length=400),
        ),
        migrations.AlterField(
            model_name='producto',
            name='descripcion',
            field=models.CharField(max_length=5000, null=True),
        ),
    ]
