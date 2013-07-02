# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'FeedType'
        db.create_table(u'aggregator_feedtype', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=250)),
            ('slug', self.gf('django.db.models.fields.SlugField')(max_length=250)),
            ('can_self_add', self.gf('django.db.models.fields.BooleanField')(default=True)),
        ))
        db.send_create_signal(u'aggregator', ['FeedType'])

        # Adding model 'Feed'
        db.create_table(u'aggregator_feed', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=500)),
            ('feed_url', self.gf('django.db.models.fields.URLField')(unique=True, max_length=500)),
            ('public_url', self.gf('django.db.models.fields.URLField')(max_length=500)),
            ('is_defunct', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('approval_status', self.gf('django.db.models.fields.CharField')(default='P', max_length=1)),
            ('feed_type', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['aggregator.FeedType'])),
            ('owner', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='owned_feeds', null=True, to=orm['users.User'])),
        ))
        db.send_create_signal(u'aggregator', ['Feed'])

        # Adding model 'FeedItem'
        db.create_table(u'aggregator_feeditem', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('feed', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['aggregator.Feed'])),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=500)),
            ('link', self.gf('django.db.models.fields.URLField')(max_length=500)),
            ('summary', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('date_modified', self.gf('django.db.models.fields.DateTimeField')()),
            ('guid', self.gf('django.db.models.fields.CharField')(unique=True, max_length=500, db_index=True)),
        ))
        db.send_create_signal(u'aggregator', ['FeedItem'])


    def backwards(self, orm):
        # Deleting model 'FeedType'
        db.delete_table(u'aggregator_feedtype')

        # Deleting model 'Feed'
        db.delete_table(u'aggregator_feed')

        # Deleting model 'FeedItem'
        db.delete_table(u'aggregator_feeditem')


    models = {
        u'aggregator.feed': {
            'Meta': {'object_name': 'Feed'},
            'approval_status': ('django.db.models.fields.CharField', [], {'default': "'P'", 'max_length': '1'}),
            'feed_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['aggregator.FeedType']"}),
            'feed_url': ('django.db.models.fields.URLField', [], {'unique': 'True', 'max_length': '500'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_defunct': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'owner': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'owned_feeds'", 'null': 'True', 'to': u"orm['users.User']"}),
            'public_url': ('django.db.models.fields.URLField', [], {'max_length': '500'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '500'})
        },
        u'aggregator.feeditem': {
            'Meta': {'ordering': "('-date_modified',)", 'object_name': 'FeedItem'},
            'date_modified': ('django.db.models.fields.DateTimeField', [], {}),
            'feed': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['aggregator.Feed']"}),
            'guid': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '500', 'db_index': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'link': ('django.db.models.fields.URLField', [], {'max_length': '500'}),
            'summary': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '500'})
        },
        u'aggregator.feedtype': {
            'Meta': {'object_name': 'FeedType'},
            'can_self_add': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '250'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '250'})
        },
        u'auth.group': {
            'Meta': {'object_name': 'Group'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        u'auth.permission': {
            'Meta': {'ordering': "(u'content_type__app_label', u'content_type__model', u'codename')", 'unique_together': "((u'content_type', u'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'projects.country': {
            'Meta': {'ordering': "['name']", 'object_name': 'Country'},
            'code': ('django.db.models.fields.CharField', [], {'max_length': '2', 'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'})
        },
        u'users.user': {
            'Meta': {'object_name': 'User'},
            'avatar': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'country': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['projects.Country']", 'null': 'True', 'blank': 'True'}),
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'unique': 'True', 'max_length': '75'}),
            'for_hire': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'github_url': ('django.db.models.fields.URLField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'gravatar_email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'null': 'True', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'location': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'user_type': ('django.db.models.fields.CharField', [], {'default': "'I'", 'max_length': '1'}),
            'website_url': ('django.db.models.fields.URLField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['aggregator']