# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('gamewebstore', '0005_auto_20160507_1506'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usergameownership',
            name='purchase_date',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]
