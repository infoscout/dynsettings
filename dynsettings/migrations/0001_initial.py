# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Bucket',
            fields=[
                ('key', models.CharField(max_length=16, serialize=False, primary_key=True)),
                ('desc', models.CharField(max_length=255, null=True, blank=True)),
                ('bucket_type', models.CharField(max_length=32, blank=True)),
                ('probability', models.IntegerField(default=0, help_text=b'Used for other apps that may choose random buckets')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='BucketSetting',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('value', models.CharField(max_length=255, blank=True)),
                ('bucket', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dynsettings.Bucket')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Setting',
            fields=[
                ('key', models.CharField(max_length=32, serialize=False, primary_key=True)),
                ('value', models.TextField(blank=True)),
                ('help_text', models.CharField(max_length=255, null=True, blank=True)),
                ('data_type', models.CharField(max_length=20, choices=[(b'STRING', b'String'), (b'INTEGER', b'Integer'), (b'FLOAT', b'Float'), (b'DECIMAL', b'Decimal'), (b'BOOLEAN', b'Boolean'), (b'LIST', b'List')])),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='bucketsetting',
            name='setting',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dynsettings.Setting'),
            preserve_default=True,
        ),
        migrations.AlterUniqueTogether(
            name='bucketsetting',
            unique_together=set([('bucket', 'setting')]),
        ),
    ]
