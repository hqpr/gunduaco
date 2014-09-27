# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Retailer'
        db.create_table('retailers', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('country', self.gf('django.db.models.fields.CharField')(max_length=255)),
        ))
        db.send_create_signal(u'products', ['Retailer'])

        # Adding model 'Category'
        db.create_table('productcategory', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('retailer', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['products.Retailer'])),
        ))
        db.send_create_signal(u'products', ['Category'])

        # Adding model 'SubCategory'
        db.create_table('productsubcategory', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('description', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('retailer', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['products.Retailer'])),
            ('category', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['products.Category'])),
        ))
        db.send_create_signal(u'products', ['SubCategory'])

        # Adding model 'SubSubCategory'
        db.create_table('productsubsubcategory', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('description', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('retailer', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['products.Retailer'])),
            ('subcategory', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['products.SubCategory'])),
        ))
        db.send_create_signal(u'products', ['SubSubCategory'])

        # Adding model 'Brand'
        db.create_table('brands', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('retailer', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['products.Retailer'])),
        ))
        db.send_create_signal(u'products', ['Brand'])

        # Adding model 'Manufacturer'
        db.create_table('manufacturer', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
        ))
        db.send_create_signal(u'products', ['Manufacturer'])

        # Adding model 'Products'
        db.create_table('products', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('retailer', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['products.Retailer'])),
            ('gtin', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('category', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['products.Category'])),
            ('subcategory', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['products.SubCategory'])),
            ('subsubcategory', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['products.SubSubCategory'])),
            ('brand', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['products.Brand'])),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('description', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('quantity', self.gf('django.db.models.fields.FloatField')()),
            ('unit_of_measure', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('url', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('creation', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('active', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('deactivation', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2014, 9, 24, 0, 0), null=True, blank=True)),
            ('packaging_type', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('manufacturer', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['products.Manufacturer'], null=True, blank=True)),
            ('manufacturer_product', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('lastfound', self.gf('django.db.models.fields.CharField')(max_length=255)),
        ))
        db.send_create_signal(u'products', ['Products'])

        # Adding model 'Prices'
        db.create_table('prices', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('product', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['products.Products'])),
            ('currency', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('price', self.gf('django.db.models.fields.FloatField')()),
            ('promotion', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('promo_text', self.gf('django.db.models.fields.TextField')()),
            ('promo_price', self.gf('django.db.models.fields.FloatField')(default=0, null=True, blank=True)),
            ('valid_from', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2014, 9, 24, 0, 0))),
            ('valid_to', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2014, 9, 24, 0, 0), null=True, blank=True)),
        ))
        db.send_create_signal(u'products', ['Prices'])


    def backwards(self, orm):
        # Deleting model 'Retailer'
        db.delete_table('retailers')

        # Deleting model 'Category'
        db.delete_table('productcategory')

        # Deleting model 'SubCategory'
        db.delete_table('productsubcategory')

        # Deleting model 'SubSubCategory'
        db.delete_table('productsubsubcategory')

        # Deleting model 'Brand'
        db.delete_table('brands')

        # Deleting model 'Manufacturer'
        db.delete_table('manufacturer')

        # Deleting model 'Products'
        db.delete_table('products')

        # Deleting model 'Prices'
        db.delete_table('prices')


    models = {
        u'products.brand': {
            'Meta': {'object_name': 'Brand', 'db_table': "'brands'"},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'retailer': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['products.Retailer']"})
        },
        u'products.category': {
            'Meta': {'object_name': 'Category', 'db_table': "'productcategory'"},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'retailer': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['products.Retailer']"})
        },
        u'products.manufacturer': {
            'Meta': {'object_name': 'Manufacturer', 'db_table': "'manufacturer'"},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        u'products.prices': {
            'Meta': {'object_name': 'Prices', 'db_table': "'prices'"},
            'currency': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'price': ('django.db.models.fields.FloatField', [], {}),
            'product': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['products.Products']"}),
            'promo_price': ('django.db.models.fields.FloatField', [], {'default': '0', 'null': 'True', 'blank': 'True'}),
            'promo_text': ('django.db.models.fields.TextField', [], {}),
            'promotion': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'valid_from': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2014, 9, 24, 0, 0)'}),
            'valid_to': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2014, 9, 24, 0, 0)', 'null': 'True', 'blank': 'True'})
        },
        u'products.products': {
            'Meta': {'object_name': 'Products', 'db_table': "'products'"},
            'active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'brand': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['products.Brand']"}),
            'category': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['products.Category']"}),
            'creation': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'deactivation': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2014, 9, 24, 0, 0)', 'null': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'gtin': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'lastfound': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'manufacturer': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['products.Manufacturer']", 'null': 'True', 'blank': 'True'}),
            'manufacturer_product': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'packaging_type': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'quantity': ('django.db.models.fields.FloatField', [], {}),
            'retailer': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['products.Retailer']"}),
            'subcategory': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['products.SubCategory']"}),
            'subsubcategory': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['products.SubSubCategory']"}),
            'unit_of_measure': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'url': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        u'products.retailer': {
            'Meta': {'object_name': 'Retailer', 'db_table': "'retailers'"},
            'country': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        u'products.subcategory': {
            'Meta': {'object_name': 'SubCategory', 'db_table': "'productsubcategory'"},
            'category': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['products.Category']"}),
            'description': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'retailer': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['products.Retailer']"})
        },
        u'products.subsubcategory': {
            'Meta': {'object_name': 'SubSubCategory', 'db_table': "'productsubsubcategory'"},
            'description': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'retailer': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['products.Retailer']"}),
            'subcategory': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['products.SubCategory']"})
        }
    }

    complete_apps = ['products']