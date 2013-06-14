# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    depends_on = (
        ("website.users", "0001_initial"),
    )

    def forwards(self, orm):
        # Adding field 'Project.creator'
        db.add_column(u'projects_project', 'creator',
                      self.gf('django.db.models.fields.related.ForeignKey')(default=1, related_name='created_projects', to=orm['users.User']),
                      keep_default=False)

        # Adding field 'Project.created'
        db.add_column(u'projects_project', 'created',
                      self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, default=datetime.datetime(2013, 6, 12, 0, 0), blank=True),
                      keep_default=False)

        # Adding field 'Project.updated'
        db.add_column(u'projects_project', 'updated',
                      self.gf('django.db.models.fields.DateTimeField')(auto_now=True, default=datetime.datetime(2013, 6, 12, 0, 0), blank=True),
                      keep_default=False)

        # Adding field 'Project.started'
        db.add_column(u'projects_project', 'started',
                      self.gf('django.db.models.fields.DateField')(default=datetime.datetime(2013, 6, 12, 0, 0)),
                      keep_default=False)

        # Adding field 'Project.description'
        db.add_column(u'projects_project', 'description',
                      self.gf('django.db.models.fields.TextField')(null=True, blank=True),
                      keep_default=False)

        # Adding field 'Project.challenges'
        db.add_column(u'projects_project', 'challenges',
                      self.gf('django.db.models.fields.TextField')(null=True, blank=True),
                      keep_default=False)

        # Adding field 'Project.audience'
        db.add_column(u'projects_project', 'audience',
                      self.gf('django.db.models.fields.TextField')(null=True, blank=True),
                      keep_default=False)

        # Adding field 'Project.technologies'
        db.add_column(u'projects_project', 'technologies',
                      self.gf('django.db.models.fields.TextField')(null=True, blank=True),
                      keep_default=False)

        # Adding field 'Project.metrics'
        db.add_column(u'projects_project', 'metrics',
                      self.gf('django.db.models.fields.TextField')(null=True, blank=True),
                      keep_default=False)

        # Adding field 'Project.num_users'
        db.add_column(u'projects_project', 'num_users',
                      self.gf('django.db.models.fields.IntegerField')(null=True, blank=True),
                      keep_default=False)

        # Adding field 'Project.repository_url'
        db.add_column(u'projects_project', 'repository_url',
                      self.gf('django.db.models.fields.URLField')(max_length=200, null=True, blank=True),
                      keep_default=False)


        # Changing field 'Project.name'
        db.alter_column(u'projects_project', 'name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=255))

    def backwards(self, orm):
        # Deleting field 'Project.creator'
        db.delete_column(u'projects_project', 'creator_id')

        # Deleting field 'Project.created'
        db.delete_column(u'projects_project', 'created')

        # Deleting field 'Project.updated'
        db.delete_column(u'projects_project', 'updated')

        # Deleting field 'Project.started'
        db.delete_column(u'projects_project', 'started')

        # Deleting field 'Project.description'
        db.delete_column(u'projects_project', 'description')

        # Deleting field 'Project.challenges'
        db.delete_column(u'projects_project', 'challenges')

        # Deleting field 'Project.audience'
        db.delete_column(u'projects_project', 'audience')

        # Deleting field 'Project.technologies'
        db.delete_column(u'projects_project', 'technologies')

        # Deleting field 'Project.metrics'
        db.delete_column(u'projects_project', 'metrics')

        # Deleting field 'Project.num_users'
        db.delete_column(u'projects_project', 'num_users')

        # Deleting field 'Project.repository_url'
        db.delete_column(u'projects_project', 'repository_url')


        # Changing field 'Project.name'
        db.alter_column(u'projects_project', 'name', self.gf('django.db.models.fields.CharField')(max_length=50, unique=True))

    models = {
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
        u'projects.project': {
            'Meta': {'ordering': "['-updated']", 'object_name': 'Project'},
            'audience': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'challenges': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'countries': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': u"orm['projects.Country']", 'null': 'True', 'blank': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'creator': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'created_projects'", 'to': u"orm['users.User']"}),
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'metrics': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'}),
            'num_users': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'repository_url': ('django.db.models.fields.URLField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50'}),
            'started': ('django.db.models.fields.DateField', [], {}),
            'technologies': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'updated': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})
        },
        u'users.user': {
            'Meta': {'object_name': 'User'},
            'country': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['projects.Country']", 'null': 'True', 'blank': 'True'}),
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'unique': 'True', 'max_length': '75'}),
            'for_hire': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'github_url': ('django.db.models.fields.URLField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
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

    complete_apps = ['projects']
