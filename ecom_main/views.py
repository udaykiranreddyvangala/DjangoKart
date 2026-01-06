from django.http import HttpResponse
from django.shortcuts import render,redirect
from store.models import Product
from cart.models import Cart,CartItem
from store.models import Product    
from cart import views
from django.core.paginator import EmptyPage,PageNotAnInteger,Paginator
from django.db.models import Q 

def home(request):
    products=Product.objects.all().filter(is_available=True).order_by('stock')
    context={
        'products':products,
    }
    return render(request,'home.html',context)

def search(request):
    keyword=request.GET.get('keyword')
    if keyword is not None:
        
        products=Product.objects.filter(Q(product_name__icontains=keyword)|Q(description__icontains=keyword)|Q(category__category_name__icontains=keyword),is_available=True)
        products_count=products.count()
        context={
            'products':products,
            'products_count':products_count,
        }
        return render(request,'search-result.html',context)
    return render(request,'search-result.html')