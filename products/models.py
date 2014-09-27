from django.db import models
from datetime import datetime


class Retailer(models.Model):
    name = models.CharField(max_length=255)
    country = models.CharField(max_length=255)

    class Meta:
        db_table = 'retailers'

    def __unicode__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(max_length=255)
    retailer = models.ForeignKey(Retailer)

    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'
        db_table = 'productcategory'

    def __unicode__(self):
        return self.name


class SubCategory(models.Model):
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    retailer = models.ForeignKey(Retailer)
    category = models.ForeignKey(Category)

    class Meta:
        verbose_name_plural = 'Sub-Categories'
        db_table = 'productsubcategory'

    def __unicode__(self):
        return self.name


class SubSubCategory(models.Model):
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    retailer = models.ForeignKey(Retailer)
    subcategory = models.ForeignKey(SubCategory)

    class Meta:
        verbose_name_plural = 'Sub-Sub-Categories'
        db_table = 'productsubsubcategory'

    def __unicode__(self):
        return self.name


class Brand(models.Model):
    name = models.CharField(max_length=255)
    retailer = models.ForeignKey(Retailer)

    class Meta:
        verbose_name = 'Brand'
        verbose_name_plural = 'Brands'
        db_table = 'brands'

    def __unicode__(self):
        return self.name


class Manufacturer(models.Model):
    name = models.CharField(max_length=255)

    class Meta:
        db_table = 'manufacturer'

    def __unicode__(self):
        return self.name


STATUS_ACTIVE = True
STATUS_NOT_ACTIVE = False


class Products(models.Model):
    retailer = models.ForeignKey(Retailer)
    gtin = models.CharField(max_length=255)
    category = models.ForeignKey(Category)
    subcategory = models.ForeignKey(SubCategory)
    subsubcategory = models.ForeignKey(SubSubCategory)
    brand = models.ForeignKey(Brand)
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    quantity = models.FloatField()
    unit_of_measure = models.CharField(max_length=255)
    url = models.CharField(max_length=255)
    creation = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=STATUS_ACTIVE)
    deactivation = models.DateTimeField(blank=True, null=True, default=datetime.now())
    packaging_type = models.CharField(max_length=255, blank=True, null=True)
    manufacturer = models.ForeignKey(Manufacturer, blank=True, null=True)
    manufacturer_product = models.IntegerField(blank=True, null=True)
    # lastfound = models.ForeignKey(LastFound)
    lastfound = models.CharField(max_length=255)

    class Meta:
        verbose_name = 'Product'
        verbose_name_plural = 'products'
        db_table = 'products'

    def __unicode__(self):
        return self.name


class Prices(models.Model):
    product = models.ForeignKey(Products)
    currency = models.CharField(max_length=255)
    price = models.FloatField()
    promotion = models.BooleanField(default=STATUS_NOT_ACTIVE)
    promo_text = models.TextField()
    promo_price = models.FloatField(default=0, blank=True, null=True)
    valid_from = models.DateField(default=datetime.now())
    valid_to = models.DateTimeField(default=datetime.now(), blank=True, null=True)

    class Meta:
        verbose_name = 'Price'
        db_table = 'prices'

    def __unicode__(self):
        return self.promotion


# class LastFound(models.Model):
#     product = models.ForeignKey(Products)
#     counter = models.IntegerField()
#
#     class Meta:
#         db_table = 'lastfound'

    # def __unicode__(self):
    #     return self.counter