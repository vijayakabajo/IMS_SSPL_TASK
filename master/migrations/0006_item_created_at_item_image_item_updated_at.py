# Generated by Django 5.1.1 on 2024-09-21 16:18

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('master', '0005_alter_item_name_alter_supplier_contact_number'),
    ]

    operations = [
        migrations.AddField(
            model_name='item',
            name='created_At',
            field=models.DateTimeField(auto_now_add=True, default=datetime.datetime(2024, 9, 21, 16, 18, 11, 647267)),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='item',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='item_images'),
        ),
        migrations.AddField(
            model_name='item',
            name='updated_At',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
