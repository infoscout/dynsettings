# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding field 'Bucket.bucket_type'
        db.add_column('dynsettings_bucket', 'bucket_type', self.gf('django.db.models.fields.CharField')(default='', max_length=32, blank=True), keep_default=False)

        # Adding field 'Bucket.probability'
        db.add_column('dynsettings_bucket', 'probability', self.gf('django.db.models.fields.IntegerField')(default=0), keep_default=False)

        # Adding unique constraint on 'BucketSetting', fields ['setting', 'bucket']
        db.create_unique('dynsettings_bucketsetting', ['setting_id', 'bucket_id'])


    def backwards(self, orm):
        
        # Removing unique constraint on 'BucketSetting', fields ['setting', 'bucket']
        db.delete_unique('dynsettings_bucketsetting', ['setting_id', 'bucket_id'])

        # Deleting field 'Bucket.bucket_type'
        db.delete_column('dynsettings_bucket', 'bucket_type')

        # Deleting field 'Bucket.probability'
        db.delete_column('dynsettings_bucket', 'probability')


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
            'value': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'})
        }
    }

    complete_apps = ['dynsettings']
