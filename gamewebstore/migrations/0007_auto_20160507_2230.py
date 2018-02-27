# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import uuid
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('gamewebstore', '0006_auto_20160507_2038'),
    ]

    operations = [
        migrations.CreateModel(
            name='Transaction',
            fields=[
                ('id', models.UUIDField(serialize=False, default=uuid.uuid4, primary_key=True, editable=False)),
                ('pending', models.BooleanField(default=True)),
                ('amount', models.DecimalField(max_digits=5, decimal_places=2)),
                ('expires', models.DateTimeField(null=True)),
                ('game', models.ForeignKey(related_name='transactions', to='gamewebstore.OnlineGame')),
                ('user', models.ForeignKey(related_name='transactions', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AlterUniqueTogether(
            name='transaction',
            unique_together=set([('user', 'game')]),
        ),
    ]
