# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-10-31 08:31
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='CmsUser',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('username', models.CharField(db_index=True, max_length=32, unique=True, verbose_name=b'\xe5\xa7\x93\xe5\x90\x8d')),
                ('email', models.EmailField(blank=True, max_length=255, unique=True)),
                ('phone', models.CharField(blank=True, max_length=11, null=True, verbose_name=b'\xe7\x94\xb5\xe8\xaf\x9d\xe5\x8f\xb7\xe7\xa0\x81')),
                ('name', models.CharField(blank=True, max_length=100, null=True, verbose_name=b'\xe4\xb8\xad\xe6\x96\x87\xe5\x90\x8d')),
                ('head_img', models.ImageField(blank=True, upload_to=b'uploads/portrait', verbose_name=b'\xe5\xa4\xb4\xe5\x83\x8f')),
                ('create_date', models.DateField(auto_now=True, verbose_name=b'\xe5\x88\x9b\xe5\xbb\xba\xe6\x97\xb6\xe9\x97\xb4')),
                ('is_active', models.BooleanField(default=True)),
                ('is_admin', models.BooleanField(default=False)),
            ],
            options={
                'verbose_name': '\u544a\u8b66\u7528\u6237',
                'verbose_name_plural': '\u544a\u8b66\u7528\u6237',
                'permissions': (('view_users', 'Can see available userlist'),),
            },
        ),
        migrations.CreateModel(
            name='Allow_Ip',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ip', models.GenericIPAddressField(unique=True)),
            ],
            options={
                'verbose_name_plural': 'Ip\u767d\u540d\u5355',
            },
        ),
        migrations.CreateModel(
            name='CmsGroup',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64, verbose_name=b'\xe9\x83\xa8\xe9\x97\xa8')),
                ('remarks', models.CharField(blank=True, max_length=64, verbose_name=b'\xe5\xa4\x87\xe6\xb3\xa8')),
            ],
            options={
                'verbose_name': '\u544a\u8b66\u7528\u6237\u7ec4',
                'verbose_name_plural': '\u544a\u8b66\u7528\u6237\u7ec4',
            },
        ),
        migrations.CreateModel(
            name='Email_Config',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('smtp_host', models.CharField(max_length=70, unique=True, verbose_name=b'\xe9\x82\xae\xe4\xbb\xb6\xe4\xb8\xbb\xe6\x9c\xba\xe9\x85\x8d\xe7\xbd\xae')),
                ('smtp_port', models.IntegerField(verbose_name=b'\xe9\x82\xae\xe4\xbb\xb6\xe7\xab\xaf\xe5\x8f\xa3\xe9\x85\x8d\xe7\xbd\xae')),
                ('smtp_user', models.CharField(max_length=70, verbose_name=b'\xe9\x82\xae\xe4\xbb\xb6\xe7\x99\xbb\xe5\xbd\x95\xe7\x94\xa8\xe6\x88\xb7')),
                ('smtp_pass', models.CharField(max_length=70, verbose_name=b'\xe9\x82\xae\xe4\xbb\xb6\xe7\x99\xbb\xe5\xbd\x95\xe5\xaf\x86\xe7\xa0\x81')),
                ('smtp_ssl', models.BooleanField(default=False, verbose_name=b'SSL')),
            ],
            options={
                'verbose_name_plural': '\u90ae\u4ef6\u8d26\u6237\u914d\u7f6e',
            },
        ),
        migrations.CreateModel(
            name='Email_Log',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.CharField(blank=True, max_length=500, null=True)),
                ('content', models.CharField(blank=True, max_length=500, null=True)),
                ('status', models.CharField(blank=True, max_length=500, null=True)),
                ('date', models.DateTimeField(auto_now_add=True, null=True)),
            ],
            options={
                'verbose_name_plural': '\u90ae\u4ef6\u65e5\u5fd7',
            },
        ),
        migrations.CreateModel(
            name='Sms_Config',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('api_key', models.CharField(max_length=70, unique=True, verbose_name=b'\xe4\xba\x91\xe7\x89\x87\xe7\xbd\x91\xe7\x9f\xad\xe4\xbf\xa1\xe5\xaf\x86\xe9\x92\xa5\xe9\x85\x8d\xe7\xbd\xae')),
            ],
            options={
                'verbose_name_plural': '\u4e91\u7247\u7f51\u77ed\u4fe1\u5bc6\u94a5',
            },
        ),
        migrations.CreateModel(
            name='Sms_Log',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('phone', models.CharField(blank=True, max_length=500, null=True)),
                ('content', models.CharField(blank=True, max_length=500, null=True)),
                ('status', models.CharField(blank=True, max_length=500, null=True)),
                ('date', models.DateTimeField(auto_now_add=True, null=True)),
            ],
            options={
                'verbose_name_plural': '\u77ed\u4fe1\u65e5\u5fd7',
            },
        ),
        migrations.AddField(
            model_name='cmsuser',
            name='group',
            field=models.ManyToManyField(to='webhook.CmsGroup', verbose_name=b'\xe6\x89\x80\xe5\xb1\x9e\xe5\x91\x8a\xe8\xad\xa6\xe7\xbb\x84'),
        ),
    ]
