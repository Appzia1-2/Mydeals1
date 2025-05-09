# Generated by Django 5.1.1 on 2025-03-18 07:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('oman_app', '0028_villa_furnished'),
    ]

    operations = [
        migrations.AddField(
            model_name='villa',
            name='land_area',
            field=models.DecimalField(decimal_places=2, default=1, max_digits=10, verbose_name='Land Area (sqft)'),
            preserve_default=False,
        ),
    ]
