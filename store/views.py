from django.shortcuts import render
from .models import Product
# Create your views here.
def store(request,slug=None):
    products=None
    
    if slug!=None:
        products=Product.objects.filter(category__slug=slug,is_available=True)
    else:    
        products=Product.objects.all().filter(is_available=True)
    products_count=products.count()
    context={
        'products':products,
        'count':products_count,
    }
    
    return render(request,'store.html',context)

def product_detail(request,slug):
    product=Product.objects.get(slug=slug)
    context={
        'product':product,
    }
    
    return render(request,'product_detail.html',context)