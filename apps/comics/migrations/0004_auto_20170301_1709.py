# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-03-02 01:09
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('comics', '0003_auto_20170301_1601'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='image',
            field=models.ImageField(default='pic_folder/None/no-img.jpg', upload_to='pic_folder'),
        ),
    ]
