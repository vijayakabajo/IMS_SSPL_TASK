# Generated by Django 5.1.1 on 2024-09-20 07:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('master', '0002_remove_item_quantity_remove_item_status_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='item',
            name='status',
            field=models.SmallIntegerField(default=1),
        ),
        migrations.AddField(
            model_name='supplier',
            name='status',
            field=models.SmallIntegerField(default=0),
        ),
    ]
