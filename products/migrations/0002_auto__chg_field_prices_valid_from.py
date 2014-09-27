# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):

        # Changing field 'Prices.valid_from'
        db.alter_column('prices', 'valid_from', self.gf('django.db.models.fields.DateField')())

    def backwards(self, orm):

        # Changing field 'Prices.valid_from'
        db.alter_column('prices', 'valid_from', self.gf('django.db.models.fields.DateTimeField')())

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
            'valid_from': ('django.db.models.fields.DateField', [], {'default': 'datetime.datetime(2014, 9, 24, 0, 0)'}),
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