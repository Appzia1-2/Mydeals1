# Generated by Django 5.0.1 on 2025-02-27 10:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('oman_app', '0004_advertisement'),
    ]

    operations = [
        migrations.AddField(
            model_name='advertisement',
            name='url',
            field=models.URLField(blank=True, max_length=500, null=True),
        ),
    ]
