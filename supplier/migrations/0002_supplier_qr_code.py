# Generated by Django 4.2.5 on 2024-09-16 06:07

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('supplier', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='supplier',
            name='qr_code',
            field=models.ImageField(default=django.utils.timezone.now, upload_to='supplier/qr_codes'),
            preserve_default=False,
        ),
    ]
