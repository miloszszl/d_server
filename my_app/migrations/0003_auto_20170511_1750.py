# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-05-11 15:50
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('my_app', '0002_page_test_redirection'),
    ]

    operations = [
        migrations.AddField(
            model_name='button',
            name='global_working_percentage',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=4, null=True),
        ),
        migrations.AddField(
            model_name='button',
            name='last_month_working_percentage',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=4, null=True),
        ),
        migrations.AddField(
            model_name='page',
            name='global_working_percentage',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=4, null=True),
        ),
        migrations.AddField(
            model_name='page',
            name='last_month_working_percentage',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=4, null=True),
        ),
    ]
