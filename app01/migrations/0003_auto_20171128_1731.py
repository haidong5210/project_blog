# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2017-11-28 17:31
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app01', '0002_auto_20171123_1943'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='webartilecla',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='app01.Web_artile_cla', verbose_name='文章所述主页文章类'),
        ),
    ]