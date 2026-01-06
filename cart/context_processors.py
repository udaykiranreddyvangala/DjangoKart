from .models import Cart,CartItem
from . import views
def get_count(request):
    count=0
    try:
        cart=Cart.objects.get(cart_id=views._cart_id(request))
        cart_items=CartItem.objects.filter(cart=cart)
        for cart_item in cart_items:
            count+=cart_item.quantity
    except Exception as e:
        pass
    
    return {'count':count}