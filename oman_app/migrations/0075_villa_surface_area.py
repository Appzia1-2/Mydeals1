# Generated by Django 5.0.1 on 2025-03-20 14:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('oman_app', '0074_remove_villa_number_of_floors'),
    ]

    operations = [
        migrations.AddField(
            model_name='villa',
            name='surface_area',
            field=models.DecimalField(decimal_places=2, default=1, max_digits=10, verbose_name='Surface Area'),
            preserve_default=False,
        ),
    ]
