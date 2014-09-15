from django.contrib import admin

from products.models import Products, Retailer, Brand, Category, SubCategory, SubSubCategory, Manufacturer, Prices


class ProductsAdmin(admin.ModelAdmin):
    search_fields = ('name', 'active')


class PriceAdmin(admin.ModelAdmin):
    list_display = ('product', 'price')
    search_fields = ('product', 'promo_text')

admin.site.register(Products, ProductsAdmin)
admin.site.register(Retailer)
admin.site.register(Brand)
admin.site.register(Category)
admin.site.register(SubCategory)
admin.site.register(SubSubCategory)
admin.site.register(Manufacturer)
admin.site.register(Prices, PriceAdmin)
