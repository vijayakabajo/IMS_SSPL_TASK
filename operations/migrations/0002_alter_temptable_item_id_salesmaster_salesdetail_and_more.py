# Generated by Django 5.1.1 on 2024-09-28 14:57

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('master', '0006_item_created_at_item_image_item_updated_at'),
        ('operations', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='temptable',
            name='item_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='master.item', unique=True),
        ),
        migrations.CreateModel(
            name='SalesMaster',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('bill_number', models.CharField(max_length=20)),
                ('bill_date', models.DateField()),
                ('sub_total', models.DecimalField(decimal_places=2, max_digits=10)),
                ('created_at', models.DateField(auto_now_add=True)),
                ('status', models.SmallIntegerField(default=1)),
                ('seller', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='master.supplier')),
            ],
        ),
        migrations.CreateModel(
            name='SalesDetail',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('item_price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('quantity', models.IntegerField()),
                ('items_total', models.DecimalField(decimal_places=2, max_digits=10)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('status', models.SmallIntegerField(default=1)),
                ('item', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='master.item')),
                ('sales_master', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sales_details', to='operations.salesmaster')),
            ],
        ),
        migrations.CreateModel(
            name='SalesTempTable',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('item_price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('quantity', models.IntegerField()),
                ('items_total', models.DecimalField(decimal_places=2, max_digits=10)),
                ('item', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='master.item')),
                ('sales_master', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sales_details_temp', to='operations.salesmaster')),
            ],
        ),
    ]
