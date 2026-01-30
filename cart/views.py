from django.shortcuts import render,get_object_or_404,redirect
from django.http import  HttpResponse
from store.models import Product,Variation
from .models import Cart,CartItem
# Create your views here.

def _cart_id(request):
    cart_id=request.session.session_key
    
    if not cart_id:
        cart_id=request.session.create()
    return cart_id
    
def add_cart(request,product_id):
    
    product=get_object_or_404(Product,id=product_id)
    
    product_variations=[]
    
    if request.method=='POST':
        
        for item in request.POST:
            key=item
            value=request.POST[key]
            try:
                varition=Variation.objects.get(product=product,variation_category__icontains=key,variation_value__icontains=value)
                product_variations.append(varition)
            except Variation.DoesNotExist:
                pass
    
                 
    try:
        cart=Cart.objects.get(cart_id=_cart_id(request))
    except Cart.DoesNotExist:
        cart=Cart.objects.create(cart_id=_cart_id(request))
        cart.save()
        
    print(cart)
        
    # cart_item_exists=CartItem.objects.filter(product=product,cart=cart).exists()
    # if cart_item_exists:
    cart_items=CartItem.objects.filter(product=product,cart=cart)
        
    existing_variations=[]
    cart_item_id=[]
    
    for cart_item in cart_items:
        curr_variations=list(cart_item.variations.all())
        # curr_variations.sort()
        existing_variations.append(curr_variations)
        cart_item_id.append(cart_item.id)
    
    if product_variations in existing_variations:
        index=existing_variations.index(product_variations)
        cart_item_id=cart_item_id[index]
        cart_item=CartItem.objects.get(id=cart_item_id)
        cart_item.quantity+=1
        cart_item.save()
    else:
        cart_item=CartItem.objects.create(
        product=product,
        cart=cart,
        quantity=1
    )    
    cart_item.variations.set(product_variations)
    cart_item.save()
    
    # else:
    #     cart_item=CartItem.objects.create(
    #         product=product,
    #         cart=cart,
    #         quantity=1
    #     )    
    #     cart_item.variations.set(product_variations)
    #     cart_item.save()
    
    return redirect('cart')

def increment_cart_item(request,cart_item_id):
    cart_item=CartItem.objects.get(id=cart_item_id)
    cart_item.quantity+=1
    cart_item.save()
    return redirect('cart')

def remove_cart(request,cart_item_id):
    cart_item=CartItem.objects.get(id=cart_item_id)
    
    if cart_item.quantity>1:
        cart_item.quantity-=1
        cart_item.save()
    else:
        cart_item.delete()
    return redirect('cart')

def remove_cart_item(request,cart_item_id):
    cart_item=CartItem.objects.get(id=cart_item_id)
    cart_item.delete()
    return redirect('cart')


def cart(request,total=0,grand_total=0,quantity=0,tax=0,cart_items=None):
    
    try:
        cart=Cart.objects.get(cart_id=_cart_id(request))
        cart_items=CartItem.objects.filter(cart=cart,is_active=True)
        for cart_item in cart_items:
            total+=(cart_item.quantity*cart_item.product.price)
            quantity+=cart_item.quantity
        tax=(2*total/100)
        grand_total=total+tax
    except Cart.DoesNotExist:
        pass
    
    context={
        'total':total,
        'tax':tax,
        'grand_total':grand_total,
        'quantity':quantity,
        'cart_items':cart_items,
    }
    return render(request,'cart.html',context)