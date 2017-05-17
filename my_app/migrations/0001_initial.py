# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-05-07 17:02
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Batch',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('levels', models.IntegerField()),
            ],
            options={
                'db_table': 'Batch',
            },
        ),
        migrations.CreateModel(
            name='Button',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('locator', models.CharField(max_length=5000)),
            ],
            options={
                'db_table': 'Buttons',
            },
        ),
        migrations.CreateModel(
            name='Page',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('address', models.CharField(max_length=5000)),
                ('weight', models.IntegerField(blank=True, null=True)),
                ('weight_w_pictures', models.IntegerField(blank=True, null=True)),
                ('encoding', models.CharField(blank=True, max_length=50)),
                ('cookies_present', models.BooleanField(default=None)),
                ('avg_download_time', models.IntegerField(blank=True)),
                ('force_test', models.BooleanField(default=False)),
            ],
            options={
                'db_table': 'Pages',
            },
        ),
        migrations.CreateModel(
            name='Page_Connection',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('page_1', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='page_connection_1', to='my_app.Page')),
                ('page_2', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='page_connection_2', to='my_app.Page')),
            ],
            options={
                'db_table': 'Pages_Connections',
            },
        ),
        migrations.CreateModel(
            name='Page_Host',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('domain_name', models.CharField(max_length=2000)),
                ('ipv4', models.CharField(max_length=15)),
            ],
            options={
                'db_table': 'Page_hosts',
            },
        ),
        migrations.CreateModel(
            name='Page_Test',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_working', models.BooleanField(default=True)),
                ('response_code', models.IntegerField()),
                ('download_time', models.IntegerField(verbose_name=2000)),
                ('page', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='page_test_p', to='my_app.Page')),
            ],
            options={
                'db_table': 'Pages_Tests',
            },
        ),
        migrations.CreateModel(
            name='T_P_B',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_working', models.BooleanField()),
                ('button', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='t_p_b_b', to='my_app.Button')),
                ('page_test', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='p_t_b_pt', to='my_app.Page_Test')),
            ],
            options={
                'db_table': 'T_P_B',
            },
        ),
        migrations.CreateModel(
            name='Test',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField(default=django.utils.timezone.now)),
            ],
            options={
                'db_table': 'Tests',
            },
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ipv4', models.CharField(max_length=15)),
                ('transfer_speed', models.DecimalField(decimal_places=2, max_digits=7)),
                ('mac_address', models.CharField(max_length=16)),
            ],
            options={
                'db_table': 'Users',
            },
        ),
        migrations.AddField(
            model_name='test',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='test_u', to='my_app.User'),
        ),
        migrations.AddField(
            model_name='page_test',
            name='test',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='page_test_t', to='my_app.Test'),
        ),
        migrations.AddField(
            model_name='page',
            name='host',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='page_h', to='my_app.Page_Host'),
        ),
        migrations.AddField(
            model_name='button',
            name='page',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='button_p', to='my_app.Page'),
        ),
        migrations.AddField(
            model_name='batch',
            name='page',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='batch_p', to='my_app.Page'),
        ),
        migrations.AddField(
            model_name='batch',
            name='test',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='batch_t', to='my_app.Test'),
        ),
    ]
