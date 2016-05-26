# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-05-26 06:15
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('interface', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Build',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ref', models.TextField()),
                ('sha', models.TextField()),
                ('status', models.TextField(choices=[(b'success', b'success'), (b'error', b'error'), (b'pending', b'pending'), (b'cancelled', b'cancelled')], default=b'pending')),
                ('result', models.TextField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('finished_at', models.DateTimeField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Repo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('owner', models.TextField()),
                ('name', models.TextField()),
                ('webhook_url', models.URLField(blank=True, null=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='repos', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.DeleteModel(
            name='Result',
        ),
        migrations.AddField(
            model_name='build',
            name='repo',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='interface.Repo'),
        ),
    ]
