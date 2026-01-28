from .models import Cart,CartItem
from .views import _cart_id

def count(request):
    count=0
    
    if 'admin'  in request.path:
        return {}
    try:
        cart_items=CartItem.objects.filter(cart__cart_id=_cart_id(request))
        for cart_item in cart_items:
            count+=cart_item.quantity
    except CartItem.DoesNotExist:
        pass
    
    return dict(count=count)