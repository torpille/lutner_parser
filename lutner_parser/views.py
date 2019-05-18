from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.core.paginator import Paginator
from ._utils import pagin
from django.contrib.auth.decorators import login_required
from lutner_parser.models import *
# Create your views here.

@login_required
def balalaiker_catalog(request):
    qs = Product.objects.filter(brandname__name = "БалалайкерЪ").order_by('article')
    cat = []
    for i in qs.order_by('category'):
        if i.category not in cat:
            cat.append(i.category)
    f_art = request.GET.get('filter_art')
    f_nam = request.GET.get('filter_name')
    f_cat = request.GET.get('filter_cat')
    f_sort = request.GET.get('filter_sort')
    f_ch_cat = request.GET.get('change_cat')
    if (f_ch_cat) and (f_ch_cat != "all"):
        qs = qs.filter(category = f_ch_cat)
    elif (f_ch_cat == "all"):
         qs = Product.objects.filter(brandname__name = "БалалайкерЪ").order_by('article')    
    if f_art:
        qs = qs.filter(article__icontains = f_art)
    if f_nam:
        qs = qs.filter(name__icontains = f_nam)
    if f_cat:
        qs = qs.filter(category__name__icontains = f_cat)  
    if f_sort:
        qs = qs.order_by(f_sort)  

    a = dict()
    for i in qs:
        stat = Statistics.objects.filter(product = i).order_by('-date')
        f1 = 0
        f2 = 0
        for j in stat[1:2]:
            if j.count > i.count:
                f1 = 1
            elif j.count < i.count:
                f1 = 2
            if j.price > i.price:
                f2 = 1
            elif j.price < i.price:
                f2 = 2
            a[i.id] = [f1, f2]

    return render(request, 'catalog/balalaiker.html', {
        'qw': qs,
        'a': a,
        'cat': cat,
    })
"""
@login_required
def balalaiker_catalog(request):
    qs = Statistics.objects.filter(product__brandname__name = "БалалайкерЪ").order_by('-date')
    prod = Product.objects.filter(brandname__name = "БалалайкерЪ").order_by('article')
    a = dict()
    for i in prod:
        stat = Statistics.objects.filter(product = i).order_by('-date')
        for j in stat[1:]:
            qs = qs.exclude(id=j.id)


    return render(request, 'catalog/balalaiker1.html', {
        'qw': qs,
        'a': a,
    })
"""
@login_required
def one_product(request, pk):
    prod = get_object_or_404(Product, id=pk)
    stat = Statistics.objects.filter(product = prod).order_by('-date')
    return render(request, 'catalog/oneprod.html', {
        'prod': prod,
        'stat': stat,
    })

def redir(request):
    return HttpResponseRedirect('/balalaiker/')