# Generated by Django 5.0.4 on 2024-05-16 08:06

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0002_alter_vendor_staff'),
    ]

    operations = [
        migrations.AddField(
            model_name='driver',
            name='owner',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='inventory.vendor'),
        ),
    ]
