# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('gamewebstore', '0007_auto_20160507_2230'),
    ]

    operations = [
        migrations.AlterField(
            model_name='onlinegamescore',
            name='score',
            field=models.FloatField(default=0.0),
        ),
    ]
