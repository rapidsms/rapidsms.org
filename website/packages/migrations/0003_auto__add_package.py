# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Package'
        db.create_table(u'packages_package', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=50)),
            ('slug', self.gf('django.db.models.fields.SlugField')(max_length=50)),
            ('pkg_type', self.gf('django.db.models.fields.SmallIntegerField')(default=0)),
            ('pypi_url', self.gf('django.db.models.fields.URLField')(max_length=200)),
            ('has_tests', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('has_docs', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal(u'packages', ['Package'])

        # Adding M2M table for field countries on 'Package'
        db.create_table(u'packages_package_countries', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('package', models.ForeignKey(orm[u'packages.package'], null=False)),
            ('country', models.ForeignKey(orm[u'packages.country'], null=False))
        ))
        db.create_unique(u'packages_package_countries', ['package_id', 'country_id'])


    def backwards(self, orm):
        # Deleting model 'Package'
        db.delete_table(u'packages_package')

        # Removing M2M table for field countries on 'Package'
        db.delete_table('packages_package_countries')


    models = {
        u'packages.country': {
            'Meta': {'ordering': "['name']", 'object_name': 'Country'},
            'code': ('django.db.models.fields.CharField', [], {'max_length': '2', 'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'})
        },
        u'packages.package': {
            'Meta': {'object_name': 'Package'},
            'countries': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': u"orm['packages.Country']", 'null': 'True', 'blank': 'True'}),
            'has_docs': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'has_tests': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '50'}),
            'pkg_type': ('django.db.models.fields.SmallIntegerField', [], {'default': '0'}),
            'pypi_url': ('django.db.models.fields.URLField', [], {'max_length': '200'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50'})
        }
    }

    complete_apps = ['packages']