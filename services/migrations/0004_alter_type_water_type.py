# Generated by Django 4.1.3 on 2022-12-13 09:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('services', '0003_alter_product_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='type',
            name='water_type',
            field=models.CharField(max_length=50),
        ),
    ]
