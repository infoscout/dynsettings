# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'Setting'
        db.create_table('dynsettings_setting', (
            ('key', self.gf('django.db.models.fields.CharField')(max_length=32, primary_key=True)),
            ('value', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
            ('help_text', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('data_type', self.gf('django.db.models.fields.CharField')(max_length=20)),
        ))
        db.send_create_signal('dynsettings', ['Setting'])


    def backwards(self, orm):
        
        # Deleting model 'Setting'
        db.delete_table('dynsettings_setting')


    models = {
        'dynsettings.setting': {
            'Meta': {'object_name': 'Setting'},
            'data_type': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'help_text': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'key': ('django.db.models.fields.CharField', [], {'max_length': '32', 'primary_key': 'True'}),
            'value': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'})
        }
    }

    complete_apps = ['dynsettings']
