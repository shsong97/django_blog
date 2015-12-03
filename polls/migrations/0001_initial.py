# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Choice',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('choice_text', models.CharField(max_length=200, verbose_name=b'\xec\x84\xa0\xed\x83\x9d\xed\x95\xad\xeb\xaa\xa9')),
                ('votes', models.IntegerField(default=0, verbose_name=b'\xed\x88\xac\xed\x91\x9c\xec\x88\x98')),
            ],
        ),
        migrations.CreateModel(
            name='Poll',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('question', models.CharField(max_length=200, verbose_name=b'\xec\xa7\x88\xeb\xac\xb8')),
                ('total_count', models.IntegerField(default=0, verbose_name=b'\xec\xa0\x84\xec\xb2\xb4\xed\x88\xac\xed\x91\x9c\xec\x88\x98')),
            ],
        ),
        migrations.CreateModel(
            name='PollList',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=200, verbose_name=b'\xec\xa0\x9c\xeb\xaa\xa9')),
                ('pub_date', models.DateTimeField(default=django.utils.timezone.now, verbose_name=b'\xeb\x93\xb1\xeb\xa1\x9d\xec\x9d\xbc')),
                ('start_date', models.DateField(default=django.utils.timezone.now, verbose_name=b'\xec\x8b\x9c\xec\x9e\x91\xec\x9d\xbc')),
                ('end_date', models.DateField(default=django.utils.timezone.now, verbose_name=b'\xec\xa2\x85\xeb\xa3\x8c\xec\x9d\xbc')),
                ('status', models.CharField(default=b'OP', max_length=2, verbose_name=b'\xec\x83\x81\xed\x83\x9c', choices=[(b'OP', b'Open'), (b'CL', b'Closed')])),
            ],
        ),
        migrations.AddField(
            model_name='poll',
            name='poll_list',
            field=models.ForeignKey(to='polls.PollList'),
        ),
        migrations.AddField(
            model_name='choice',
            name='poll',
            field=models.ForeignKey(to='polls.Poll'),
        ),
    ]
