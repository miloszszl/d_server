# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-05-13 16:16
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('my_app', '0007_auto_20170513_1742'),
    ]

    operations = [
        migrations.AlterField(
            model_name='button',
            name='page',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='button_p', to='my_app.Page'),
        ),
        migrations.AlterField(
            model_name='t_p_b',
            name='button',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='t_p_b_b', to='my_app.Button'),
        ),
        migrations.AlterField(
            model_name='t_p_b',
            name='page_test',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='p_t_b_pt', to='my_app.Page_Test'),
        ),
        migrations.AlterField(
            model_name='test',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='test_u', to='my_app.User'),
        ),
    ]
