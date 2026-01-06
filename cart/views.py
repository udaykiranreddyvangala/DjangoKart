from django.shortcuts import render,get_object_or_404,redirect
from .models import Cart,CartItem
from store.models import Product
from django.core.exceptions import ObjectDoesNotExist
from  django.http import HttpResponse
from  store.models import Variation
# Create your views here.
def _cart_id(request):
    cart=request.session.session_key
    if not cart:
        cart=request.session.create
    return cart

def variation_key(variations):
    return sorted([v.id for v in variations])


def add_cart(request,product_id):
    product=get_object_or_404(Product,id=product_id)
    product_variation=[]
    if request.method=='POST':
        for item in request.POST:
            key=item
            value=request.POST[key]
            
            try:
                variation=Variation.objects.get(product=product,variation_category__iexact=key,variation_value__iexact=value)
                product_variation.append(variation)
            except:
                pass
        
    cart_id=_cart_id(request)
    cart, created = Cart.objects.get_or_create(cart_id=cart_id)

    cart_items = CartItem.objects.filter(product=product, cart=cart)

    if cart_items.exists():
        ex_var_list = []
        item_ids = []

        for item in cart_items:
            ex_var_list.append(
                variation_key(item.variations.all())
            )
            item_ids.append(item.id)

        if variation_key(product_variation) in ex_var_list:
            index = ex_var_list.index(variation_key(product_variation))
            item_id = item_ids[index]

            item = CartItem.objects.get(id=item_id)
            item.quantity += 1
            item.save()
        else:
            cart_item = CartItem.objects.create(
                product=product,
                cart=cart,
                quantity=1
            )
            cart_item.variations.add(*product_variation)
    else:
        cart_item = CartItem.objects.create(
            product=product,
            cart=cart,
            quantity=1
        )
        cart_item.variations.add(*product_variation)

      
    return redirect('cart')

def remove(request,id):
    cart_item=CartItem.objects.get(id=id)
    cart_item.delete()
    return redirect('cart')

def remove_cart(request,id):
    cart_item=CartItem.objects.get(id=id)
    if cart_item.quantity>1:
        cart_item.quantity-=1
        cart_item.save()
    else:
        cart_item.delete()
    return redirect('cart')
    
def cart(request,total=0,quantity=0,tax=0,grand_total=0,cart_items=None,variations=None):
    try:
        cart=Cart.objects.get(cart_id=_cart_id(request))
        cart_items=CartItem.objects.filter(cart=cart,is_active=True)
        for item in cart_items:
            quantity+=item.quantity
            total+=(item.sub_total())
            
        tax=(10*total)/100
        grand_total=total+tax
    except ObjectDoesNotExist:
            pass
        
    context={
            'cart_items':cart_items,
            'quantity':quantity,
            'total':total,
            'tax':tax,
            'grand_total':grand_total,
        }
    return render(request,'cart.html',context)
