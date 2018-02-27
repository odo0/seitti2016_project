# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', serialize=False, primary_key=True)),
                ('name', models.CharField(max_length=255, unique=True)),
            ],
            options={
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='Company',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', serialize=False, primary_key=True)),
                ('name', models.CharField(max_length=255, unique=True)),
                ('user', models.ManyToManyField(to=settings.AUTH_USER_MODEL, related_name='companies')),
            ],
            options={
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='OnlineGame',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', serialize=False, primary_key=True)),
                ('name', models.CharField(max_length=255, unique=True)),
                ('active', models.BooleanField()),
                ('url', models.URLField()),
                ('price', models.IntegerField()),
                ('categories', models.ForeignKey(to='gamewebstore.Category', related_name='games')),
                ('company', models.ForeignKey(to='gamewebstore.Company', related_name='games')),
            ],
            options={
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='OnlineGameSaveState',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', serialize=False, primary_key=True)),
                ('data', models.BinaryField()),
                ('game', models.ForeignKey(to='gamewebstore.OnlineGame', related_name='saves')),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL, related_name='saves')),
            ],
        ),
        migrations.CreateModel(
            name='OnlineGameScore',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', serialize=False, primary_key=True)),
                ('score', models.BigIntegerField()),
                ('game', models.ForeignKey(to='gamewebstore.OnlineGame', related_name='scores')),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL, related_name='scores')),
            ],
        ),
    ]
