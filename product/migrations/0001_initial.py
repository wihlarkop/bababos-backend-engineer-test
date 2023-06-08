# Generated by Django 4.2.1 on 2023-06-07 16:17

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Sku',
            fields=[
                ('sku_id', models.CharField(max_length=20, primary_key=True, serialize=False, unique=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'db_table': 'sku',
            },
        ),
        migrations.CreateModel(
            name='UnitOfMeasure',
            fields=[
                ('name', models.CharField(max_length=10, primary_key=True, serialize=False, unique=True)),
            ],
            options={
                'db_table': 'uom',
            },
        ),
        migrations.CreateModel(
            name='PriceList',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('price', models.FloatField()),
                ('stock', models.IntegerField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('sku_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='product.sku')),
            ],
            options={
                'db_table': 'price_list',
            },
        ),
    ]