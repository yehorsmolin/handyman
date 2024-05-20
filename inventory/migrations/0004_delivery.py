# Generated by Django 5.0.4 on 2024-05-16 10:09

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0003_driver_owner'),
    ]

    operations = [
        migrations.CreateModel(
            name='Delivery',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=120)),
                ('description', models.TextField(blank=True, null=True)),
                ('pick_up_address', models.TextField(blank=True, null=True)),
                ('delivery_address', models.CharField(blank=True, max_length=200, null=True)),
                ('boxes', models.TextField(blank=True, null=True)),
                ('dimensions', models.TextField(blank=True, null=True)),
                ('weight', models.TextField(blank=True, null=True)),
                ('is_active', models.BooleanField(default=True)),
                ('delivery_date', models.DateTimeField()),
                ('driver', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='inventory.driver')),
                ('order', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='inventory.order')),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='inventory.vendor')),
            ],
            options={
                'verbose_name_plural': 'Deliveries',
            },
        ),
    ]