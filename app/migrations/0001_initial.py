# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2018-01-04 06:49
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='License',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('license_number', models.CharField(max_length=100, null=True, verbose_name='license_number')),
                ('name', models.CharField(max_length=255, null=True, verbose_name='name')),
                ('license_type', models.CharField(max_length=255, null=True, verbose_name='license_type')),
                ('primary_status', models.CharField(max_length=255, null=True, verbose_name='primary_status')),
                ('previous_names', models.CharField(max_length=255, null=True, verbose_name='previous_names')),
                ('address', models.CharField(max_length=255, null=True, verbose_name='address')),
                ('issuance_date', models.CharField(max_length=100, null=True, verbose_name='issuance_date')),
                ('expiration_date', models.CharField(max_length=100, null=True, verbose_name='expiration_date')),
                ('current_date_time', models.CharField(max_length=100, null=True, verbose_name='current_date_time')),
                ('source_url', models.CharField(max_length=255, null=True, verbose_name='source_url')),
            ],
        ),
    ]
