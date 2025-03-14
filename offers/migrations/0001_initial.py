# Generated by Django 5.1.6 on 2025-03-07 06:37

import django.utils.timezone
import django_countries.fields
import tinymce.models
import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('last_modify_time', models.DateTimeField(default=django.utils.timezone.now)),
                ('name', models.CharField(max_length=30, unique=True)),
                ('slug', models.SlugField(blank=True, max_length=30)),
            ],
            options={
                'verbose_name': 'Category',
                'verbose_name_plural': 'Categories',
            },
        ),
        migrations.CreateModel(
            name='Complaint',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('last_modify_time', models.DateTimeField(default=django.utils.timezone.now)),
                ('text', models.TextField(verbose_name='Complaint text')),
                ('status', models.CharField(choices=[('pe', 'Pending'), ('re', 'Reviewed'), ('ac', 'Accepted'), ('de', 'Declined')], default='pe', max_length=2)),
                ('admin_comment', models.TextField(blank=True, null=True, verbose_name='Admin Comment')),
            ],
            options={
                'verbose_name': 'Complaint',
                'verbose_name_plural': 'Complaints',
                'ordering': ['-created_at'],
            },
        ),
        migrations.CreateModel(
            name='Offer',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('last_modify_time', models.DateTimeField(default=django.utils.timezone.now)),
                ('title', models.CharField(max_length=100, unique=True, verbose_name='Title')),
                ('body', tinymce.models.HTMLField()),
                ('slug', models.SlugField(blank=True, max_length=200, unique=True)),
                ('image', models.ImageField(blank=True, default='media/default_offer.png', null=True, upload_to='offer_img')),
                ('status', models.CharField(choices=[('pe', 'Pending'), ('pu', 'Published'), ('re', 'Rejected')], default='pe', max_length=2)),
                ('country', django_countries.fields.CountryField(blank=True, max_length=2, null=True)),
                ('url', models.URLField(blank=True, null=True)),
                ('is_premium', models.BooleanField(default=False)),
                ('premium_at', models.DateTimeField(blank=True, null=True)),
            ],
            options={
                'verbose_name': 'Offer',
                'verbose_name_plural': 'Offers',
                'db_table_comment': 'Offer table braviss',
                'get_latest_by': 'created_at',
            },
        ),
    ]
