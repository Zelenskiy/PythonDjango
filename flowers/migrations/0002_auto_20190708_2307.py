# Generated by Django 2.2.3 on 2019-07-08 20:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('flowers', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='simpleaddflower',
            name='photo',
            field=models.ImageField(blank=True, null=True, upload_to='user_images'),
        ),
    ]