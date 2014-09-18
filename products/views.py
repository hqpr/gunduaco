# -*- coding: utf-8 -*-

from django.shortcuts import render
from .models import Products, Prices, Brand, Category, Retailer
from django.contrib.auth.decorators import login_required
from django.db.models import Count
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


"""
https://docs.djangoproject.com/en/1.5/topics/auth/default/#how-to-log-a-user-in
http://www.highcharts.com/demo/dynamic-update
http://extendbootstrap.com/

The following was specified:
User interactions / Selection & Search Criteria

- Ability to search through the product table with multiple criteria with
the posibility to add filters after search results.--> The multiple
criteria where not defined

- Search on a 4 Level Hierarchy ( after Level 1 has been choosen, only the
matching level 2’s should be shown in --> Retailer, Category, sub category
& subsubcategory

The following might not have been clear: the X-axe should hold a timeline,
the Y-ace should indicate the number of promotions in a certain period, the
Bar(s) should represent the selected group for a certain retailer, each
other retailer should have a different color.

The following was not defined: ---> aggregation of multiple individual
products, resulting in aggregation of the number of promotions in a period

The following was not defined: ---> the setting to set the period for each
column

-----------------------------------DONE----------------------------------
- Productname search with free text

- 2 field with numeric value’s ( logical search criteria Between, higher
etc) --> These are the dates

"""


def index(request):
    products = Products.objects.filter(active=True)[:20]
    context = {'products': 'products'}
    return render(request, 'products/index.html', context)


@login_required
def charts(request):
    products = Prices.objects.filter(promotion=True).values('product').annotate(Count('product'))
    c = products.count()
    brands = Brand.objects.filter(products__prices__promotion=True).values('name', 'id').distinct()
    context = {'products': products, 'c': c, 'brands': brands}
    return render(request, 'products/charts.html', context)


@login_required
def charts_brand(request, id):
    products = Products.objects.filter(brand=id)
    title = Brand.objects.get(id=id)
    c = products.count()
    charts = Prices.objects.filter(product=products).filter(promotion=True)\
        .values('product', 'valid_from', 'product__retailer').annotate(Count('product')).annotate(Count('product__retailer'))
    chart_values = charts.count()
    context = {'products': products, 'c': c, 'title': title, 'charts': charts, 'chart_values': chart_values}
    return render(request, 'products/chart_by_brand.html', context)


@login_required
def product(request, id):
    product = Products.objects.get(id=id)
    context = {'product': product}
    return render(request, 'products/product.html', context)


@login_required
def category(request, id):
    products = Products.objects.filter(category=id)
    title = Category.objects.get(id=id)
    charts = Prices.objects.filter(product=products).filter(promotion=True).values('promotion', 'valid_from').annotate(Count('valid_from')).annotate(Count('promotion'))
    paginator = Paginator(products, 10)
    page = request.GET.get('page')
    try:
        products = paginator.page(page)
    except PageNotAnInteger:
        products = paginator.page(1)
    except EmptyPage:
        products = paginator.page(paginator.num_pages)
    context = {'products': products, 'title': title, 'charts': charts}
    return render(request, 'products/category.html', context)


@login_required
def categories(request):
    cats = Category.objects.all()
    context = {'cats': cats}
    return render(request, 'products/categories.html', context)


@login_required
def search_form(request):
    return render(request, 'base.html')


@login_required
def search(request):
    errors = []
    if 'q' in request.GET:
        q = request.GET['q']
        if not q:
            errors.append('You did not specify a query')
        else:
            product = Products.objects.filter(name__icontains=q)
            return render(request, 'products/search_results.html',
                {'product': product, 'query': q})
    return render(request, 'products/index.html',
        {'errors': errors})


@login_required
def datesearch(request):
    return render(request, 'products/search_by_date.html')


def search_by_date(request):
    errors = []
    if request.GET:
        start = request.GET['s']
        start = start.split('/')
        start = '%s-%s-%s' % (start[2], start[0], start[1])
        end = request.GET['e']
        try:
            end = end.split('/')
            end = '%s-%s-%s' % (end[2], end[0], end[1])
        except:
            end = ''
        if not start and end:
            errors.append('No parameters')
        else:
            result = Prices.objects.filter(valid_from__gte=start, valid_from__lte=end)
            # paginator = Paginator(result, 10)
            # page = request.GET.get('page')
            # try:
            #     result = paginator.page(page)
            # except PageNotAnInteger:
            #     result = paginator.page(1)
            # except EmptyPage:
            #     result = paginator.page(paginator.num_pages)
            product = {'result': result, 's': start, 'e': end}
            return render(request, 'products/search_results.html', product)
    else:
        errors.append('')
        return render(request, 'products/index.html',
        {'errors': errors})