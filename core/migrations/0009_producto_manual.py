# Generated by Django 4.2 on 2023-05-13 14:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0008_rename_diametro_producto_altavoz_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='producto',
            name='manual',
            field=models.CharField(blank=True, default='N/A', max_length=400),
        ),
    ]
