# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Delivery'
        db.create_table('django_aws_tools_deliveries', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('modified_at', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('sns_topic', self.gf('django.db.models.fields.CharField')(max_length=350)),
            ('sns_messageid', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('mail_timestamp', self.gf('django.db.models.fields.DateTimeField')()),
            ('mail_id', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('mail_from', self.gf('django.db.models.fields.EmailField')(max_length=75)),
            ('address', self.gf('django.db.models.fields.EmailField')(max_length=75)),
            ('feedback_id', self.gf('django.db.models.fields.CharField')(max_length=100, null=True, blank=True)),
            ('feedback_timestamp', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('smtp_response', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('reporting_mta', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
        ))
        db.send_create_signal(u'django_aws_tools', ['Delivery'])


        # Changing field 'Complaint.feedback_id'
        db.alter_column('django_aws_tools_complaints', 'feedback_id', self.gf('django.db.models.fields.CharField')(max_length=100, null=True))

        # Changing field 'Complaint.feedback_timestamp'
        db.alter_column('django_aws_tools_complaints', 'feedback_timestamp', self.gf('django.db.models.fields.DateTimeField')(null=True))

        # Changing field 'Bounce.feedback_id'
        db.alter_column('django_aws_tools_bounces', 'feedback_id', self.gf('django.db.models.fields.CharField')(max_length=100, null=True))

        # Changing field 'Bounce.feedback_timestamp'
        db.alter_column('django_aws_tools_bounces', 'feedback_timestamp', self.gf('django.db.models.fields.DateTimeField')(null=True))

    def backwards(self, orm):
        # Deleting model 'Delivery'
        db.delete_table('django_aws_tools_deliveries')


        # Changing field 'Complaint.feedback_id'
        db.alter_column('django_aws_tools_complaints', 'feedback_id', self.gf('django.db.models.fields.CharField')(default=None, max_length=100))

        # Changing field 'Complaint.feedback_timestamp'
        db.alter_column('django_aws_tools_complaints', 'feedback_timestamp', self.gf('django.db.models.fields.DateTimeField')(default=None))

        # Changing field 'Bounce.feedback_id'
        db.alter_column('django_aws_tools_bounces', 'feedback_id', self.gf('django.db.models.fields.CharField')(default=None, max_length=100))

        # Changing field 'Bounce.feedback_timestamp'
        db.alter_column('django_aws_tools_bounces', 'feedback_timestamp', self.gf('django.db.models.fields.DateTimeField')(default=None))

    models = {
        u'django_aws_tools.bounce': {
            'Meta': {'object_name': 'Bounce', 'db_table': "'django_aws_tools_bounces'"},
            'action': ('django.db.models.fields.CharField', [], {'db_index': 'True', 'max_length': '150', 'null': 'True', 'blank': 'True'}),
            'address': ('django.db.models.fields.EmailField', [], {'max_length': '75'}),
            'bounce_subtype': ('django.db.models.fields.CharField', [], {'max_length': '50', 'db_index': 'True'}),
            'bounce_type': ('django.db.models.fields.CharField', [], {'max_length': '50', 'db_index': 'True'}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'diagnostic_code': ('django.db.models.fields.CharField', [], {'max_length': '150', 'null': 'True', 'blank': 'True'}),
            'feedback_id': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'feedback_timestamp': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'hard': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'db_index': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'mail_from': ('django.db.models.fields.EmailField', [], {'max_length': '75'}),
            'mail_id': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'mail_timestamp': ('django.db.models.fields.DateTimeField', [], {}),
            'modified_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'reporting_mta': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'sns_messageid': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'sns_topic': ('django.db.models.fields.CharField', [], {'max_length': '350'}),
            'status': ('django.db.models.fields.CharField', [], {'db_index': 'True', 'max_length': '150', 'null': 'True', 'blank': 'True'})
        },
        u'django_aws_tools.complaint': {
            'Meta': {'object_name': 'Complaint', 'db_table': "'django_aws_tools_complaints'"},
            'address': ('django.db.models.fields.EmailField', [], {'max_length': '75'}),
            'arrival_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'feedback_id': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'feedback_timestamp': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'feedback_type': ('django.db.models.fields.CharField', [], {'db_index': 'True', 'max_length': '150', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'mail_from': ('django.db.models.fields.EmailField', [], {'max_length': '75'}),
            'mail_id': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'mail_timestamp': ('django.db.models.fields.DateTimeField', [], {}),
            'modified_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'sns_messageid': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'sns_topic': ('django.db.models.fields.CharField', [], {'max_length': '350'}),
            'useragent': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'})
        },
        u'django_aws_tools.delivery': {
            'Meta': {'object_name': 'Delivery', 'db_table': "'django_aws_tools_deliveries'"},
            'address': ('django.db.models.fields.EmailField', [], {'max_length': '75'}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'feedback_id': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'feedback_timestamp': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'mail_from': ('django.db.models.fields.EmailField', [], {'max_length': '75'}),
            'mail_id': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'mail_timestamp': ('django.db.models.fields.DateTimeField', [], {}),
            'modified_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'reporting_mta': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'smtp_response': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'sns_messageid': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'sns_topic': ('django.db.models.fields.CharField', [], {'max_length': '350'})
        }
    }

    complete_apps = ['django_aws_tools']