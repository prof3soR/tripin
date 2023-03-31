# Generated by Django 4.1.7 on 2023-03-25 02:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_interface', '0008_category_destination_delete_destinations'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='image',
            field=models.ImageField(blank=True, upload_to='static/images'),
        ),
        migrations.AlterField(
            model_name='destination',
            name='image1',
            field=models.ImageField(blank=True, upload_to='static/images'),
        ),
        migrations.AlterField(
            model_name='destination',
            name='image2',
            field=models.ImageField(blank=True, upload_to='static/images'),
        ),
        migrations.AlterField(
            model_name='destination',
            name='image3',
            field=models.ImageField(blank=True, upload_to='static/images'),
        ),
        migrations.AlterField(
            model_name='destination',
            name='image4',
            field=models.ImageField(blank=True, upload_to='static/images'),
        ),
        migrations.AlterField(
            model_name='destination',
            name='image5',
            field=models.ImageField(blank=True, upload_to='static/images'),
        ),
    ]
