# Generated by Django 5.0.1 on 2025-03-25 06:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('oman_app', '0100_cafe_rental_period_clinic_rental_period_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='farm',
            name='additional_amenities',
            field=models.ManyToManyField(to='oman_app.additionalamenities'),
        ),
        migrations.AddField(
            model_name='farm',
            name='main_amenities',
            field=models.ManyToManyField(to='oman_app.mainamenities'),
        ),
        migrations.AddField(
            model_name='farm',
            name='nearby_location',
            field=models.ManyToManyField(to='oman_app.nearbylocation'),
        ),
    ]
