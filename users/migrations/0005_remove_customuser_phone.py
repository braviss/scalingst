# Generated by Django 5.1.6 on 2025-03-22 13:34

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_customuser_phone'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='customuser',
            name='phone',
        ),
    ]
