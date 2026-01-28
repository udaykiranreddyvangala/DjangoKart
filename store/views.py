from django.shortcuts import render
from .models import Product
from cart.models import Cart,CartItem
from cart.views import _cart_id
from django.core.paginator import EmptyPage,PageNotAnInteger,Paginator
# Create your views here.
def store(request,slug=None):
    products=None
    
    if slug!=None:
        products=Product.objects.filter(category__slug=slug,is_available=True).order_by('id')
        paginator=Paginator(products,1)
        page=request.GET.get('page')
        paged_products=paginator.get_page(page)
    else:    
        products=Product.objects.all().filter(is_available=True).order_by('id')
        paginator=Paginator(products,3)
        page=request.GET.get('page')
        paged_products=paginator.get_page(page)
        
    products_count=products.count()
    context={
        'products':paged_products,
        'product_count':products_count,
    }
    
    return render(request,'store.html',context)

def product_detail(request,slug):
    product=Product.objects.get(slug=slug)
    in_cart=CartItem.objects.filter(cart__cart_id=_cart_id(request),product=product).exists()
    context={
        'product':product,
        'in_cart':in_cart,
    }
    
    return render(request,'product_detail.html',context)