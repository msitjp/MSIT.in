# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-03-06 16:15
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0018_auto_20180305_1655'),
        ('storage', '0003_auto_20180305_1834'),
    ]

    operations = [
        migrations.CreateModel(
            name='ResearchRecord',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=300, verbose_name='Title/Topic')),
                ('type', models.CharField(choices=[('Conference', 'Conference'), ('Journal', 'Journal')], default='Conference', max_length=15, verbose_name='Conference/Journal')),
                ('nation', models.CharField(choices=[('International', 'International'), ('National', 'National')], default='International', max_length=15, verbose_name='International/National')),
                ('publisher', models.CharField(blank=True, max_length=200, null=True, verbose_name='Publisher')),
                ('isbn', models.CharField(blank=True, max_length=50, null=True, verbose_name='ISBN')),
                ('pages', models.CharField(blank=True, max_length=4, null=True, verbose_name='Page No')),
                ('year', models.CharField(max_length=4)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('faculty', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='web.Faculty')),
            ],
            options={
                'verbose_name': 'Research Paper & Conference Record',
                'verbose_name_plural': 'Research Paper & Conference Records',
            },
        ),
        migrations.AlterField(
            model_name='bookrecord',
            name='type',
            field=models.CharField(choices=[('International', 'International'), ('National', 'National')], default='International', max_length=15, verbose_name='International/National'),
        ),
    ]