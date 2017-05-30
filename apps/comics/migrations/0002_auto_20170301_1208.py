# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-03-01 20:08
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import django.db.models.manager


class Migration(migrations.Migration):

    dependencies = [
        ('comics', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Location',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('addr_street', models.CharField(max_length=100)),
                ('street_two', models.CharField(max_length=100)),
                ('addr_city', models.CharField(max_length=100)),
                ('addr_state', models.CharField(max_length=20)),
                ('addr_zip', models.IntegerField()),
            ],
        ),
        migrations.AlterModelManagers(
            name='order',
            managers=[
                ('orderManager', django.db.models.manager.Manager()),
            ],
        ),
        migrations.AlterModelManagers(
            name='product',
            managers=[
                ('productManager', django.db.models.manager.Manager()),
            ],
        ),
        migrations.RemoveField(
            model_name='order',
            name='addr_city',
        ),
        migrations.RemoveField(
            model_name='order',
            name='addr_state',
        ),
        migrations.RemoveField(
            model_name='order',
            name='addr_street',
        ),
        migrations.RemoveField(
            model_name='order',
            name='street_two',
        ),
        migrations.RemoveField(
            model_name='user',
            name='addr_city',
        ),
        migrations.RemoveField(
            model_name='user',
            name='addr_state',
        ),
        migrations.RemoveField(
            model_name='user',
            name='addr_street',
        ),
        migrations.RemoveField(
            model_name='user',
            name='addr_zip',
        ),
        migrations.RemoveField(
            model_name='user',
            name='street_two',
        ),
        migrations.AddField(
            model_name='location',
            name='order',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='shipping_location', to='comics.Order'),
        ),
        migrations.AddField(
            model_name='location',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='user_location', to='comics.User'),
        ),
    ]
