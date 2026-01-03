from django.shortcuts import render,get_object_or_404
from django.http import HttpResponse
from .models import Product
from category.models import Category
# Create your views here.
def store(request):
    products=Product.objects.all().filter(is_available=True)
    products_count=products.count()
    context={
        'products':products,
        'products_count':products_count,
    }
    return render(request,'store/store.html',context)

def products_by_category(request,slug):
    req_category=get_object_or_404(Category,slug=slug)
    products=Product.objects.filter(category=req_category,is_available=True)
    products_count=products.count()
    context={
        'products':products,
        'products_count':products_count,
    }
    return render(request,'store/store.html',context)

def product_details(request,slug):
    req_product=get_object_or_404(Product,slug=slug)
    context={
        'req_product':req_product,
    }
    return render(request,'product-detail.html',context)