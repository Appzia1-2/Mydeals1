# Generated by Django 5.1.1 on 2025-03-22 12:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('oman_app', '0096_rename_location_foreign_country'),
    ]

    operations = [
        migrations.AddField(
            model_name='commercial',
            name='rental_period',
            field=models.CharField(blank=True, choices=[('daily', 'Daily'), ('weekly', 'Weekly'), ('monthly', 'Monthly'), ('yearly', 'Yearly')], max_length=10, null=True, verbose_name='Rental Period'),
        ),
    ]
