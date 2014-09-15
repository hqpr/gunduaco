from django.shortcuts import render
from .models import Products, Prices
from django.contrib.auth.decorators import login_required


"""
https://docs.djangoproject.com/en/1.5/topics/auth/default/#how-to-log-a-user-in
http://stackoverflow.com/questions/15933748/bootstrap-responsive-charts-and-graphs
http://extendbootstrap.com/
"""


def index(request):
    products = Products.objects.filter(active=True)[:20]
    context = {'products': products}
    return render(request, 'products/index.html', context)

@login_required
def price(request):
    price = Prices.objects.get(id=5)
    context = {'price': price}
    return render(request, 'products/charts.html', context)

