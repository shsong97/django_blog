# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone
from django.conf import settings
import django_markdown.models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Blog',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('blog_title', models.CharField(max_length=200, verbose_name=b'Title')),
                ('contents', django_markdown.models.MarkdownField()),
                ('pub_date', models.DateTimeField(default=django.utils.timezone.now, verbose_name=b'Pub Date')),
                ('like_count', models.IntegerField(default=0, verbose_name=b'Like')),
                ('view_count', models.IntegerField(default=0, verbose_name=b'View')),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('tag_title', models.CharField(max_length=100, verbose_name=b'Tag')),
                ('blog', models.ManyToManyField(to='blog.Blog')),
            ],
        ),
    ]
