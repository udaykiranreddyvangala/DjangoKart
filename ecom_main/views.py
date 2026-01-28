from django.http import HttpResponse
from django.shortcuts import render,redirect
from store.models import Product
from django.db.models import Q

def home(request):
    products=Product.objects.all().filter(is_available=True)
    context={
        'products':products,
    }
    return render(request,'home.html',context)

def search(request):
    if request.method=='GET':
        keyword=request.GET.get('keyword')
        if keyword:
            products=Product.objects.filter(Q(product_name__icontains=keyword)|Q(description__icontains=keyword),is_available=True).order_by('-created_date')
            product_count=products.count()
        else:
            pass
    context={
        'products':products,
        'product_count':product_count,
    }
    return render(request,'store.html',context)