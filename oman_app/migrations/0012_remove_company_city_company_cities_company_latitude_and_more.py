# Generated by Django 5.1.5 on 2025-03-07 04:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('oman_app', '0011_remove_drivingtraining_latitude_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='company',
            name='city',
        ),
        migrations.AddField(
            model_name='company',
            name='cities',
            field=models.TextField(default=1, max_length=250),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='company',
            name='latitude',
            field=models.FloatField(default=1),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='company',
            name='longitude',
            field=models.FloatField(default=1),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='company',
            name='regions',
            field=models.CharField(choices=[('MS', 'Muscat'), ('DH', 'Dhofar'), ('BT', 'Batinah'), ('DA', 'Dakhiliyah'), ('SH', 'Sharqiyah'), ('BR', 'Buraimi'), ('ZU', 'Zufar'), ('MW', 'Musandam'), ('WR', 'Wusta')], default='MS', max_length=250),
        ),
    ]
