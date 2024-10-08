# Generated by Django 5.1 on 2024-08-14 06:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Hotel_info', '0002_propertyimage_caption_alter_propertyimage_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='amenity',
            name='name',
            field=models.CharField(max_length=1000),
        ),
        migrations.AlterField(
            model_name='location',
            name='latitude',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='location',
            name='longitude',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='location',
            name='name',
            field=models.CharField(max_length=1000),
        ),
        migrations.AlterField(
            model_name='location',
            name='type',
            field=models.CharField(choices=[('country', 'Country'), ('state', 'State'), ('city', 'City')], max_length=500),
        ),
        migrations.AlterField(
            model_name='property',
            name='property_id',
            field=models.CharField(max_length=150, unique=True),
        ),
        migrations.AlterField(
            model_name='property',
            name='title',
            field=models.CharField(max_length=1000),
        ),
    ]
