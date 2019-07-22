# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2019-07-22 09:12
from __future__ import unicode_literals

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('storage', '0014_auto_20180319_1731'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bookrecord',
            name='isbn',
            field=models.CharField(max_length=50, null=True, verbose_name='ISBN'),
        ),
        migrations.AlterField(
            model_name='bookrecord',
            name='pages',
            field=models.CharField(max_length=10, null=True, verbose_name='Total Pages'),
        ),
        migrations.AlterField(
            model_name='bookrecord',
            name='publisher',
            field=models.CharField(max_length=200, null=True, verbose_name='Publisher'),
        ),
        migrations.AlterField(
            model_name='fdprecord',
            name='duration',
            field=models.CharField(help_text='Number of days', max_length=5, null=True),
        ),
        migrations.AlterField(
            model_name='researchrecord',
            name='indexing',
            field=models.CharField(choices=[('SCI/SCIE', 'SCI/SCIE'), ('Scopus', 'Scopus'), ('Google Scholars', 'Google Scholars'), ('Not Applicable', 'Not Applicable'), ('Others', 'Others')], default='SCI/SCIE', max_length=10),
        ),
        migrations.AlterField(
            model_name='researchrecord',
            name='isbn',
            field=models.CharField(max_length=50, null=True, validators=[django.core.validators.RegexValidator('^[0-9-]*$')], verbose_name='ISBN/ISSN'),
        ),
        migrations.AlterField(
            model_name='researchrecord',
            name='issue',
            field=models.CharField(default='', max_length=100, null=True, verbose_name='Issue'),
        ),
        migrations.AlterField(
            model_name='researchrecord',
            name='name_of_conference',
            field=models.CharField(default='', max_length=300, null=True, verbose_name='Name of Conference/Journal'),
        ),
        migrations.AlterField(
            model_name='researchrecord',
            name='pages',
            field=models.CharField(max_length=10, null=True, validators=[django.core.validators.RegexValidator('^[0-9-]*$')], verbose_name='Page No'),
        ),
        migrations.AlterField(
            model_name='researchrecord',
            name='publisher',
            field=models.CharField(max_length=200, null=True, verbose_name='Publisher'),
        ),
        migrations.AlterField(
            model_name='researchrecord',
            name='volume',
            field=models.CharField(default='', max_length=100, null=True, verbose_name='Volume'),
        ),
        migrations.AlterField(
            model_name='researchrecord',
            name='year',
            field=models.DateField(null=True, verbose_name='Month Year'),
        ),
    ]
