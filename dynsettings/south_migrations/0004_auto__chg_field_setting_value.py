# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):

        # Changing field 'Setting.value'
        db.alter_column('dynsettings_setting', 'value', self.gf('django.db.models.fields.TextField')())

    def backwards(self, orm):

        # Changing field 'Setting.value'
        db.alter_column('dynsettings_setting', 'value', self.gf('django.db.models.fields.CharField')(max_length=255))

    models = {
        'dynsettings.bucket': {
            'Meta': {'object_name': 'Bucket'},
            'bucket_type': ('django.db.models.fields.CharField', [], {'max_length': '32', 'blank': 'True'}),
            'desc': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'key': ('django.db.models.fields.CharField', [], {'max_length': '16', 'primary_key': 'True'}),
            'probability': ('django.db.models.fields.IntegerField', [], {'default': '0'})
        },
        'dynsettings.bucketsetting': {
            'Meta': {'unique_together': "(('bucket', 'setting'),)", 'object_name': 'BucketSetting'},
            'bucket': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['dynsettings.Bucket']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'setting': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['dynsettings.Setting']"}),
            'value': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'})
        },
        'dynsettings.setting': {
            'Meta': {'object_name': 'Setting'},
            'data_type': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'help_text': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'key': ('django.db.models.fields.CharField', [], {'max_length': '32', 'primary_key': 'True'}),
            'value': ('django.db.models.fields.TextField', [], {'blank': 'True'})
        }
    }

    complete_apps = ['dynsettings']