# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('gamewebstore', '0004_auto_20160507_0031'),
    ]

    operations = [
        migrations.AddField(
            model_name='onlinegame',
            name='description',
            field=models.TextField(default=''),
        ),
        migrations.AddField(
            model_name='usergameownership',
            name='purchase_date',
            field=models.DateField(auto_now_add=True, default=datetime.datetime(2016, 5, 7, 12, 6, 44, 467272, tzinfo=utc)),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='onlinegamescore',
            name='score',
            field=models.BigIntegerField(default=0),
        ),
        migrations.AlterUniqueTogether(
            name='onlinegamesavestate',
            unique_together=set([('user', 'game')]),
        ),
        migrations.AlterUniqueTogether(
            name='onlinegamescore',
            unique_together=set([('user', 'game')]),
        ),
        migrations.AlterUniqueTogether(
            name='usergameownership',
            unique_together=set([('user', 'game')]),
        ),
    ]
