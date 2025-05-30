# Generated by Django 5.1.1 on 2025-03-19 05:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('oman_app', '0042_land_facade_land_lister_type_land_property_mortgage_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='land',
            name='zoned_for',
            field=models.CharField(choices=[('residential', 'Residential'), ('commercial', 'Commercial'), ('agricultural', 'Agricultural'), ('industrial', 'Industrial')], default=1, max_length=100, verbose_name='Zoned For'),
            preserve_default=False,
        ),
    ]
