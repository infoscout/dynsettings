# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'Bucket'
        db.create_table('dynsettings_bucket', (
            ('key', self.gf('django.db.models.fields.CharField')(max_length=16, primary_key=True)),
            ('desc', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
        ))
        db.send_create_signal('dynsettings', ['Bucket'])

        # Adding model 'BucketSetting'
        db.create_table('dynsettings_bucketsetting', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('bucket', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['dynsettings.Bucket'])),
            ('setting', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['dynsettings.Setting'])),
            ('value', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
        ))
        db.send_create_signal('dynsettings', ['BucketSetting'])


    def backwards(self, orm):
        
        # Deleting model 'Bucket'
        db.delete_table('dynsettings_bucket')

        # Deleting model 'BucketSetting'
        db.delete_table('dynsettings_bucketsetting')


    models = {
        'dynsettings.bucket': {
            'Meta': {'object_name': 'Bucket'},
            'desc': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'key': ('django.db.models.fields.CharField', [], {'max_length': '16', 'primary_key': 'True'})
        },
        'dynsettings.bucketsetting': {
            'Meta': {'object_name': 'BucketSetting'},
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
