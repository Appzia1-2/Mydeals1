# Generated by Django 5.1.1 on 2025-03-19 09:42

import django.db.models.deletion
import django.utils.timezone
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('oman_app', '0059_shopimage_shopvideo_shop'),
    ]

    operations = [
        migrations.CreateModel(
            name='CafeImage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='Cafe/images/', verbose_name='Image')),
            ],
        ),
        migrations.CreateModel(
            name='CafeVideo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('video', models.FileField(upload_to='Cafe/videos/', verbose_name='Video')),
            ],
        ),
        migrations.CreateModel(
            name='Cafe',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('property_title', models.CharField(max_length=255, verbose_name='Property Title')),
                ('price', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='Price (OMR)')),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('regions', models.CharField(choices=[('MS', 'Muscat'), ('DH', 'Dhofar'), ('BT', 'Batinah'), ('DA', 'Dakhiliyah'), ('SH', 'Sharqiyah'), ('BR', 'Buraimi'), ('ZU', 'Zufar'), ('MW', 'Musandam'), ('WR', 'Wusta')], default='MS', max_length=250)),
                ('cities', models.TextField(max_length=250)),
                ('latitude', models.FloatField()),
                ('longitude', models.FloatField()),
                ('location', models.TextField(max_length=250)),
                ('plot_area', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='Plot Area')),
                ('description', models.TextField(verbose_name='Property Description')),
                ('listing_type', models.CharField(choices=[('sell', 'Sell'), ('rent', 'Rent')], default='sell', max_length=10, verbose_name='Listing Type')),
                ('status', models.CharField(choices=[('pending', 'Pending'), ('approved', 'Approved'), ('rejected', 'Rejected'), ('soldout', 'Soldout')], default='pending', max_length=20, verbose_name='Approval Status')),
                ('property_mortgage', models.CharField(choices=[('yes', 'Yes'), ('no', 'No')], default='no', max_length=3, verbose_name='Property Mortgage')),
                ('lister_type', models.CharField(choices=[('agent', 'Agent'), ('landlord', 'Landlord')], max_length=10, verbose_name='Lister Type')),
                ('property', models.CharField(choices=[('complete', 'Complete'), ('under_construction', 'Under Construction')], default='under_construction', max_length=20, verbose_name='Property Status')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='Cafe', to=settings.AUTH_USER_MODEL)),
                ('images', models.ManyToManyField(blank=True, related_name='Cafe', to='oman_app.cafeimage', verbose_name='Images')),
                ('videos', models.ManyToManyField(blank=True, related_name='Cafe', to='oman_app.cafevideo', verbose_name='Videos')),
            ],
        ),
    ]
