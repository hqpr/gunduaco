# -*- coding: utf-8 -*-

from django.shortcuts import render
from .models import Products, Prices, Brand, Category, Retailer, SubCategory, SubSubCategory
from django.contrib.auth.decorators import login_required
from django.db.models import Count
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
import datetime


"""
https://docs.djangoproject.com/en/1.5/topics/auth/default/#how-to-log-a-user-in
http://www.highcharts.com/demo/dynamic-update
http://extendbootstrap.com/

http://simplyargh.blogspot.com/2012/04/python-27-django-14-on-bluehost.html

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
            brands = Products.objects.filter(id__in=product).filter(active=True).values('brand__name', 'brand').distinct()
            context = {'product': product, 'query': q, 'brands': brands}
            return render(request, 'products/search_results.html', context)
    return render(request, 'products/index.html',
        {'errors': errors})


@login_required
def datesearch(request):
    return render(request, 'products/search_by_date.html')


@login_required
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
            result = Prices.objects.filter(valid_from__gte=start, valid_from__lte=end).filter(promotion=True)\
                .filter(product__active=True).values('product__name', 'product__id').distinct()
            brands = Prices.objects.filter(valid_from__gte=start, valid_from__lte=end).filter(promotion=True)\
                .filter(product__active=True).values('product__brand__name', 'product__brand__id').distinct()
            categories = Prices.objects.filter(valid_from__gte=start, valid_from__lte=end).filter(promotion=True)\
                .filter(product__active=True).values('product__category__name', 'product__category__id').distinct()
            subcategories = Prices.objects.filter(valid_from__gte=start, valid_from__lte=end).filter(promotion=True)\
                .filter(product__active=True).values('product__subcategory__name', 'product__subcategory__id').distinct()
            subsubcategories = Prices.objects.filter(valid_from__gte=start, valid_from__lte=end).filter(promotion=True)\
                .filter(product__active=True).values('product__subsubcategory__name', 'product__subsubcategory__id').distinct()
            product = {'result': result,
                       's': start,
                       'e': end,
                       'brands': brands,
                       'categories': categories,
                       'subcategories': subcategories,
                       'subsubcategories': subsubcategories}

            return render(request, 'products/search_results.html', product)
    else:
        errors.append('')
        return render(request, 'products/index.html', {'errors': errors})


@login_required
def custom(request):
    if request.POST:
        ids = request.POST.getlist('product_id')
        start = request.POST['valid_from']
        end = request.POST['valid_to']
        try:
            brand = request.POST['brand_id']
        except:
            brand = None
        try:
            category = request.POST['category_id']
        except:
            category = None
        try:
            subcategory = request.POST['subcategory_id']
        except:
            subcategory = None

        if brand:
            products = Prices.objects.filter(product__id__in=ids).filter(promotion=True).filter(valid_from__gte=start)\
                .filter(valid_from__lte=end).values('product__name', 'promotion', 'valid_from', 'product__id')\
                .annotate(Count('product__name')).filter(product__active=True).order_by('-valid_from')\
                .filter(product__brand_id=brand)\

            brand = Brand.objects.get(id=brand)
            context = {'products': products, 'start': start, 'end': end, 'brand': brand}
            return render(request, 'products/custom.html', context)

        elif category:
            products = Prices.objects.filter(product__id__in=ids).filter(promotion=True).filter(valid_from__gte=start)\
                .filter(valid_from__lte=end).values('product__name', 'promotion', 'valid_from', 'product__id')\
                .annotate(Count('product__name')).filter(product__active=True).order_by('-valid_from')\
                .filter(product__category_id=category)
            category = Category.objects.get(id=category)
            context = {'products': products, 'start': start, 'end': end, 'category': category}
            return render(request, 'products/custom.html', context)

        elif subcategory:
            products = Prices.objects.filter(product__id__in=ids).filter(promotion=True).filter(valid_from__gte=start)\
                .filter(valid_from__lte=end).values('product__name', 'promotion', 'valid_from', 'product__id')\
                .annotate(Count('product__name')).filter(product__active=True).order_by('-valid_from')\
                .filter(product__subcategory_id=subcategory)

            subcategory = SubCategory.objects.get(id=subcategory)
            context = {'products': products, 'start': start, 'end': end, 'subcategory': subcategory}
            return render(request, 'products/custom.html', context)

        elif brand and category:
            products = Prices.objects.filter(product__id__in=ids).filter(promotion=True).filter(valid_from__gte=start)\
                .filter(valid_from__lte=end).values('product__name', 'promotion', 'valid_from', 'product__id')\
                .annotate(Count('product__name')).filter(product__active=True).order_by('-valid_from')\
                .filter(product__category_id=category).filter(product__brand_id=brand)

            category = Category.objects.get(id=category)
            brand = Brand.objects.get(id=brand)
            context = {'products': products, 'start': start, 'end': end, 'category': category, 'brand': brand}
            return render(request, 'products/custom.html', context)
        else:
            products = Prices.objects.filter(product__id__in=ids).filter(promotion=True).filter(valid_from__gte=start)\
                .filter(valid_from__lte=end).values('product__name', 'promotion', 'valid_from', 'product__id')\
                .annotate(Count('product__name')).filter(product__active=True).order_by('-valid_from')
            context = {'products': products, 'start': start, 'end': end, 'ids': ids}
            return render(request, 'products/custom.html', context)


@login_required
def piebrand(request):
    pie1 = Products.objects.filter(prices__promotion=1).filter(retailer_id=1).values('brand__name').\
        annotate(Count('name')).order_by('-name__count').filter(active=True, prices__valid_from=datetime.datetime.today())
    pie1_tt = Products.objects.filter(prices__promotion=1).filter(retailer_id=1).values('brand__name').\
        annotate(Count('name')).order_by('-name__count').filter(active=True, prices__valid_from=datetime.datetime.today())[:10]
    pie2 = Products.objects.filter(prices__promotion=1).filter(retailer_id=2).values('brand__name').\
        annotate(Count('name')).order_by('-name__count').filter(active=True, prices__valid_from=datetime.datetime.today())
    pie2_tt = Products.objects.filter(prices__promotion=1).filter(retailer_id=2).values('brand__name').\
        annotate(Count('name')).order_by('-name__count').filter(active=True, prices__valid_from=datetime.datetime.today())[:10]
    pie3 = Products.objects.filter(prices__promotion=1).filter(retailer_id=3).values('brand__name').\
        annotate(Count('name')).order_by('-name__count').filter(active=True, prices__valid_from=datetime.datetime.today())
    pie3_tt = Products.objects.filter(prices__promotion=1).filter(retailer_id=3).values('brand__name').\
        annotate(Count('name')).order_by('-name__count').filter(active=True, prices__valid_from=datetime.datetime.today())[:10]
    pie4 = Products.objects.filter(prices__promotion=1).filter(retailer_id=4).values('brand__name').\
        annotate(Count('name')).order_by('-name__count').filter(active=True, prices__valid_from=datetime.datetime.today())
    pie4_tt = Products.objects.filter(prices__promotion=1).filter(retailer_id=4).values('brand__name').\
        annotate(Count('name')).order_by('-name__count').filter(active=True, prices__valid_from=datetime.datetime.today())[:10]

    lst = Products.objects.filter(active=True).values('name', 'retailer__name', 'brand__name').annotate(Count('name'))[:1000]

    retailers = Retailer.objects.all()

    # paginator = Paginator(lst, 10)
    # page = request.GET.get('page')
    # try:
    #     lst = paginator.page(page)
    # except PageNotAnInteger:
    #     lst = paginator.page(1)
    # except EmptyPage:
    #     lst = paginator.page(paginator.num_pages)

    today = datetime.datetime.today()

    context = {'pie1': pie1, 'pie2': pie2,
               'pie3': pie3, 'pie4': pie4,
               'retailers': retailers,
               'pie1_tt': pie1_tt,
               'pie2_tt': pie2_tt,
               'pie3_tt': pie3_tt,
               'pie4_tt': pie4_tt,
               'lst': lst,
               'today': today}
    return render(request, 'products/piechart.html', context)

@login_required
def pie_by_retailer(request):
    if request.POST:
        retailer = request.POST['retailer']
        start = request.POST['s']
        start = start.split('/')
        start = '%s-%s-%s' % (start[2], start[0], start[1])
        end = request.POST['e']
        try:
            end = end.split('/')
            end = '%s-%s-%s' % (end[2], end[0], end[1])
        except:
            end = ''
        result = Products.objects.filter(prices__promotion=True).filter(retailer_id=retailer).values('brand__name').\
                annotate(Count('name')).order_by('-name__count').filter(active=True)\
            .filter(prices__valid_from__gte=start, prices__valid_to__lte=end)
        result__tt = Products.objects.filter(prices__promotion=True).filter(retailer_id=retailer).values('brand__name').\
                annotate(Count('name')).order_by('-name__count').filter(active=True)\
            .filter(prices__valid_from__gte=start, prices__valid_to__lte=end)[:10]
        retailers = Retailer.objects.all()
        r_name = Retailer.objects.get(id=retailer)
        context = {'result': result, 'start': start, 'r_name': r_name, 'retailers': retailers, 'result__tt': result__tt}
        return render(request, 'products/custom_pie.html', context)


@login_required
def piecategory(request):
    pie1 = Products.objects.filter(prices__promotion=1).filter(retailer_id=1).values('category__name').\
        annotate(Count('name')).order_by('name__count').filter(active=True, prices__valid_from=datetime.datetime.today())
    pie1_tt = Products.objects.filter(prices__promotion=1).filter(retailer_id=2).values('category__name').\
        annotate(Count('name')).order_by('-name__count').filter(active=True, prices__valid_from=datetime.datetime.today())[:10]
    pie2 = Products.objects.filter(prices__promotion=1).filter(retailer_id=2).values('category__name').\
        annotate(Count('name')).order_by('name__count').filter(active=True, prices__valid_from=datetime.datetime.today())
    pie2_tt = Products.objects.filter(prices__promotion=1).filter(retailer_id=2).values('category__name').\
        annotate(Count('name')).order_by('-name__count').filter(active=True, prices__valid_from=datetime.datetime.today())[:10]
    pie3 = Products.objects.filter(prices__promotion=1).filter(retailer_id=3).values('category__name').\
        annotate(Count('name')).order_by('name__count').filter(active=True, prices__valid_from=datetime.datetime.today())
    pie3_tt = Products.objects.filter(prices__promotion=1).filter(retailer_id=3).values('category__name').\
        annotate(Count('name')).order_by('-name__count').filter(active=True, prices__valid_from=datetime.datetime.today())[:10]
    pie4 = Products.objects.filter(prices__promotion=1).filter(retailer_id=4).values('category__name').\
        annotate(Count('name')).order_by('name__count').filter(active=True, prices__valid_from=datetime.datetime.today())
    pie4_tt = Products.objects.filter(prices__promotion=1).filter(retailer_id=4).values('category__name').\
        annotate(Count('name')).order_by('-name__count').filter(active=True, prices__valid_from=datetime.datetime.today())[:10]

    retailers = Retailer.objects.all()
    today = datetime.datetime.today()

    lst = Products.objects.filter(active=True).values('name', 'retailer__name', 'category__name').annotate(Count('name'))[:1000]

    context = {'pie1': pie1, 'pie2': pie2,
               'pie3': pie3, 'pie4': pie4,
               'retailers': retailers,
               'pie1_tt': pie1_tt,
               'pie2_tt': pie2_tt,
               'pie3_tt': pie3_tt,
               'pie4_tt': pie4_tt,
               'lst': lst,
               'today': today}
    return render(request, 'products/piechart_category.html', context)

@login_required
def price_analyses(request):
    products = Products.objects.filter(active=True)[:10]
    retailers = Retailer.objects.all()
    category = Category.objects.all()
    subcategory = SubCategory.objects.all()
    subsubcategory = SubSubCategory.objects.all()
    today = datetime.datetime.today()
    context = {'products': products,
               'retailers': retailers,
               'category': category,
               'subcategory': subcategory,
               'subsubcategory': subsubcategory,
               'today': today}
    return render(request, 'products/price_analyses.html', context)


@login_required
def promoanalyses_brand(request):
    retailers = Retailer.objects.all()
    brands = Brand.objects.all()
    context = {'retailers': retailers, 'brands': brands}
    return render(request, 'products/promoanalyses_brand.html', context)


@login_required
def promoanalyses(request):
    if request.POST:
        retailer = request.POST['retailer']
        brand = request.POST['brand']
        start = request.POST['s']
        start = start.split('/')
        start = '%s-%s-%s' % (start[2], start[0], start[1])
        end = request.POST['e']
        try:
            end = end.split('/')
            end = '%s-%s-%s' % (end[2], end[0], end[1])
        except:
            end = ''
        result = Products.objects.filter(prices__promotion=True, active=True, retailer_id=retailer,
                                         brand_id=brand,
                                         prices__valid_from__gte=start,
                                         prices__valid_to__lte=end).values('retailer__name', 'brand__name',
                                                                           'prices__valid_from') \
            .annotate(Count('prices__promotion'))

        context = {'result': result}
        return render(request, 'products/promoanalyses.html', context)



