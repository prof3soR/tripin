# Generated by Django 4.1.7 on 2023-03-20 15:50

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('user_interface', '0005_secretspot'),
    ]

    operations = [
        migrations.CreateModel(
            name='review_loaction',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('location_name', models.CharField(max_length=100)),
                ('trip_img1', models.ImageField(upload_to='static\\images\review_imgs')),
                ('trip_img2', models.ImageField(upload_to='static\\images\review_imgs')),
                ('trip_img3', models.ImageField(upload_to='static\\images\review_imgs')),
                ('desc', models.TextField()),
                ('rating', models.PositiveIntegerField(verbose_name=range(1, 6))),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='user_interface.profile')),
            ],
        ),
    ]
