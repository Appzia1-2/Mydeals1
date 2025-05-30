# Generated by Django 5.1.1 on 2025-03-14 06:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('oman_app', '0015_remove_drivingtraining_latitude_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='ApartmentListing',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('listing_type', models.CharField(choices=[('S', 'For Sale'), ('R', 'For Rent')], default='S', max_length=1)),
                ('rental_period', models.CharField(blank=True, choices=[('D', 'Daily'), ('W', 'Weekly'), ('M', 'Monthly'), ('Y', 'Yearly')], max_length=1, null=True)),
                ('number_of_rooms', models.PositiveIntegerField()),
                ('number_of_bathrooms', models.PositiveIntegerField()),
                ('surface_area', models.FloatField()),
                ('floor', models.PositiveIntegerField()),
                ('last_floor_with_roof', models.BooleanField(default=False)),
                ('building_age', models.PositiveIntegerField()),
                ('furnished_status', models.CharField(choices=[('F', 'Furnished'), ('SF', 'Semi Furnished'), ('UF', 'Unfurnished')], max_length=2)),
                ('video_reel', models.URLField(blank=True, null=True)),
                ('pictures', models.ImageField(blank=True, null=True, upload_to='apartment_pictures/')),
                ('cover_picture', models.ImageField(blank=True, null=True, upload_to='apartment_cover_pictures/')),
                ('solar_panels', models.BooleanField(default=False)),
                ('intercom', models.BooleanField(default=False)),
                ('central_air_conditioning', models.BooleanField(default=False)),
                ('air_conditioning', models.BooleanField(default=False)),
                ('heating', models.BooleanField(default=False)),
                ('balcony', models.BooleanField(default=False)),
                ('maid_room', models.BooleanField(default=False)),
                ('laundry_room', models.BooleanField(default=False)),
                ('built_in_wardrobes', models.BooleanField(default=False)),
                ('private_pool', models.BooleanField(default=False)),
                ('elevator', models.BooleanField(default=False)),
                ('garden', models.BooleanField(default=False)),
                ('garage_parking', models.BooleanField(default=False)),
                ('security', models.BooleanField(default=False)),
                ('staircase', models.BooleanField(default=False)),
                ('storage', models.BooleanField(default=False)),
                ('bbq_area', models.BooleanField(default=False)),
                ('emergency_backup_electricity', models.BooleanField(default=False)),
                ('nearby_pharmacy', models.BooleanField(default=False)),
                ('nearby_restaurant', models.BooleanField(default=False)),
                ('nearby_school', models.BooleanField(default=False)),
                ('nearby_supermarket', models.BooleanField(default=False)),
                ('nearby_mall', models.BooleanField(default=False)),
                ('nearby_gym', models.BooleanField(default=False)),
                ('nearby_hospital', models.BooleanField(default=False)),
                ('nearby_mosque', models.BooleanField(default=False)),
                ('nearby_dry_clean', models.BooleanField(default=False)),
                ('nearby_parking', models.BooleanField(default=False)),
                ('city', models.CharField(max_length=100)),
                ('neighborhood', models.CharField(max_length=100)),
                ('facade', models.CharField(max_length=100)),
                ('description', models.TextField()),
                ('title', models.CharField(max_length=200)),
                ('full_price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('payment_method', models.CharField(choices=[('CO', 'Cash Only'), ('CI', 'Cash or Installments'), ('IO', 'Installments Only')], max_length=2)),
                ('contact_number', models.CharField(max_length=15)),
                ('property_mortgaged', models.BooleanField(default=False)),
            ],
        ),
    ]
