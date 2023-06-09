# Generated by Django 4.2.1 on 2023-06-08 07:32

from django.db import migrations


def insert_data(apps, schema_editor):
    Supplier = apps.get_model("supplier", "Supplier")

    suppliers = [
        Supplier(supplier_id="S1-KPS-1", address="Kelurahan Klender, Kecamatan Duren Sawit", city="Jakarta Timur",
                 state="DKI Jakarta"),
        Supplier(supplier_id="S1-HSC-1", address="Mangga Dua Sel., Kecamatan Sawah Besar", city="Jakarta Pusat",
                 state="DKI Jakarta"),
        Supplier(supplier_id="S1-PSB-1", address="Tubagus Angke", city="Jakarta", state="DKI Jakarta"),
        Supplier(supplier_id="S1-SUM-1", address="Kedung Waringin, Kec. Tanah Sereal", city="Kota Bogor",
                 state="Jawa Barat"),
        Supplier(supplier_id="S1-ISB-1", address="Penjaringan", city="Jakarta Utara", state="DKI Jakarta"),
        Supplier(supplier_id="S1-FIX-1", address="Godangdia", city="Jakarta Pusat", state="DKI Jakarta"),
        Supplier(supplier_id="S1-SAM-1", address="Bantar Gebang", city="Kota Bekasi", state="Jawa Barat"),
        Supplier(supplier_id="S1-SSC-1", address="Kec. Sawah Besar", city="Jakarta Pusat", state="DKI Jakarta"),
    ]

    Supplier.objects.bulk_create(suppliers)


class Migration(migrations.Migration):
    run_before = [
        ('product', '0004_auto_20230608_1446'),
    ]

    dependencies = [
        ('supplier', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(insert_data)
    ]
