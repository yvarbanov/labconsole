# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='LabConsole',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, serialize=False, primary_key=True)),
                ('token', models.CharField(max_length=32)),
                ('username', models.CharField(max_length=20)),
                ('password', models.CharField(max_length=20)),
                ('project', models.CharField(max_length=20)),
            ],
        ),
    ]
