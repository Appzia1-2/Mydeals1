# Generated by Django 5.1.1 on 2025-03-15 06:08

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('oman_app', '0019_buildingimage_buildingvideo_wholebuilding'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='wholebuilding',
            name='images',
        ),
        migrations.RemoveField(
            model_name='wholebuilding',
            name='videos',
        ),
        migrations.RemoveField(
            model_name='wholebuilding',
            name='user',
        ),
        migrations.DeleteModel(
            name='BuildingImage',
        ),
        migrations.DeleteModel(
            name='BuildingVideo',
        ),
        migrations.DeleteModel(
            name='WholeBuilding',
        ),
    ]
