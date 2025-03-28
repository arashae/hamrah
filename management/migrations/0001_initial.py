# Generated by Django 5.0.1 on 2025-03-18 11:31

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Admin',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=255, unique=True)),
                ('password', models.CharField(max_length=255)),
                ('name', models.CharField(max_length=255)),
                ('phone_number', models.CharField(max_length=11)),
                ('is_active', models.BooleanField(default=True)),
            ],
            options={
                'db_table': 'admins',
            },
        ),
        migrations.CreateModel(
            name='Brand',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('brand', models.CharField(max_length=255, unique=True)),
            ],
            options={
                'db_table': 'brands',
            },
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category', models.CharField(max_length=255, unique=True)),
            ],
            options={
                'db_table': 'categories',
            },
        ),
        migrations.CreateModel(
            name='Company',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, unique=True)),
            ],
            options={
                'db_table': 'companies',
            },
        ),
        migrations.CreateModel(
            name='Province',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('province', models.CharField(max_length=255, unique=True)),
            ],
            options={
                'db_table': 'provinces',
            },
        ),
        migrations.CreateModel(
            name='Supplier',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=255, unique=True)),
                ('password', models.CharField(max_length=255)),
                ('name', models.CharField(max_length=255)),
                ('phone_number', models.CharField(max_length=11, null=True)),
                ('is_active', models.BooleanField(default=True)),
            ],
            options={
                'db_table': 'suppliers',
            },
        ),
        migrations.CreateModel(
            name='PortionPlan',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('MCI_portion', models.FloatField()),
                ('store_portion', models.FloatField()),
                ('supplier_portion', models.FloatField()),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='management.category')),
            ],
            options={
                'db_table': 'portion_plans',
            },
        ),
        migrations.CreateModel(
            name='City',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('city', models.CharField(max_length=255)),
                ('province', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='management.province')),
            ],
            options={
                'db_table': 'cities',
                'unique_together': {('city', 'province')},
            },
        ),
        migrations.CreateModel(
            name='Store',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=255, unique=True)),
                ('password', models.CharField(max_length=255)),
                ('name', models.CharField(max_length=255)),
                ('type', models.CharField(max_length=255)),
                ('manager', models.CharField(max_length=255)),
                ('phone_number', models.CharField(max_length=11)),
                ('address', models.CharField(max_length=512)),
                ('is_active', models.BooleanField(default=True)),
                ('city', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='management.city')),
                ('company', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='management.company')),
            ],
            options={
                'db_table': 'stores',
            },
        ),
        migrations.CreateModel(
            name='Device',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('model', models.CharField(max_length=255)),
                ('RAM', models.CharField(max_length=255, null=True)),
                ('storage', models.CharField(max_length=255, null=True)),
                ('color', models.CharField(max_length=255, null=True)),
                ('pack', models.CharField(max_length=255, null=True)),
                ('network', models.CharField(max_length=255, null=True)),
                ('is_active', models.BooleanField(default=True)),
                ('brand', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='management.brand')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='management.category')),
            ],
            options={
                'db_table': 'devices',
                'unique_together': {('category', 'brand', 'model')},
            },
        ),
    ]
