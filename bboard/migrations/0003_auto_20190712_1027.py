# Generated by Django 2.2.3 on 2019-07-12 07:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bboard', '0002_bb_photo_prev'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bb',
            name='photo',
            field=models.CharField(blank=True, max_length=250, null=True),
        ),
    ]
