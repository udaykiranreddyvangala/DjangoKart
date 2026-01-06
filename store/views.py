from django.shortcuts import render,get_object_or_404
from django.http import HttpResponse
from .models import Product
from category.models import Category
from cart.models import Cart,CartItem
from cart import views
from django.core.paginator import Paginator,EmptyPage,PageNotAnInteger

# Create your views here.
def store(request):
    products=Product.objects.all().filter(is_available=True).order_by('id')
    products_count=products.count()
    paginator=Paginator(products,3)
    page=request.GET.get('page')
    paged_products=paginator.get_page(page)
    context={
        'products':paged_products,
        'products_count':products_count,
    }
    return render(request,'store/store.html',context)

def products_by_category(request,slug):
    req_category=get_object_or_404(Category,slug=slug)
    products=Product.objects.filter(category=req_category,is_available=True).order_by('id')
    products_count=products.count()
    paginator=Paginator(products,1)
    page=request.GET.get('page')
    paged_products=paginator.get_page(page)
    context={
        'products':paged_products,
        'products_count':products_count,
    }
    return render(request,'store/store.html',context)

def product_details(request,slug):
    req_product=get_object_or_404(Product,slug=slug)
    in_cart=True
    try:
        cart=Cart.objects.get(cart_id=views._cart_id(request))
        cart_item=CartItem.objects.get(cart=cart,product=req_product)
    except Exception as e:
        in_cart=False
    context={
        'req_product':req_product,
        'in_cart':in_cart,
    }
    
    return render(request,'product-detail.html',context)