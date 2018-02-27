# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('gamewebstore', '0003_auto_20160505_2127'),
    ]

    operations = [
        migrations.AlterField(
            model_name='onlinegame',
            name='price',
            field=models.DecimalField(decimal_places=2, max_digits=5),
        ),
    ]
