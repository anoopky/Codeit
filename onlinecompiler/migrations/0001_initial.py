# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Questions',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, auto_created=True, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('title', models.CharField(max_length=255)),
                ('description', models.TextField()),
                ('input_public', models.TextField()),
                ('output_public', models.TextField()),
                ('explanation', models.TextField()),
                ('verification', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Result',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, auto_created=True, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('code', models.TextField()),
                ('language', models.TextField()),
                ('score', models.TextField()),
                ('execution_time', models.TextField()),
                ('status', models.TextField()),
                ('questionId', models.ForeignKey(to='onlinecompiler.Questions')),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ('execution_time', 'score'),
            },
        ),
        migrations.CreateModel(
            name='TestCases',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, auto_created=True, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('input_private', models.TextField()),
                ('output_private', models.TextField()),
                ('questionId', models.ForeignKey(to='onlinecompiler.Questions')),
            ],
        ),
        migrations.AlterUniqueTogether(
            name='result',
            unique_together=set([('user', 'questionId')]),
        ),
    ]
