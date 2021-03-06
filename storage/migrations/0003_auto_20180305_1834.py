# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-03-05 13:04
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('storage', '0002_auto_20180305_1703'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bookrecord',
            name='count',
            field=models.CharField(blank=True, max_length=3, null=True, verbose_name='Total Count'),
        ),
        migrations.AlterField(
            model_name='bookrecord',
            name='isbn',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name='ISBN'),
        ),
        migrations.AlterField(
            model_name='bookrecord',
            name='pages',
            field=models.CharField(blank=True, max_length=4, null=True, verbose_name='Page No'),
        ),
        migrations.AlterField(
            model_name='bookrecord',
            name='publisher',
            field=models.CharField(blank=True, max_length=200, null=True, verbose_name='Publisher'),
        ),
    ]
