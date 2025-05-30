# Generated by Django 5.0.1 on 2025-03-20 09:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('oman_app', '0067_alter_land_facade_alter_land_regions_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='villa',
            name='number_of_floors',
            field=models.PositiveIntegerField(choices=[('1_floor', '1 Floor'), ('2_floors', '2 Floors'), ('3_floors', '3 Floors'), ('4_floors', '4 Floors'), ('5_floors', '5+ Floors')], verbose_name='Number of Floors'),
        ),
    ]
