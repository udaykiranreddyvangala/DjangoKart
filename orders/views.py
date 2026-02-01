from django.shortcuts import render,redirect
from django.http import  HttpResponse,JsonResponse
from cart.models import CartItem
from django.contrib import messages
from .forms import OrderForm
from .models import Order,Payment,OrderProduct
import datetime
import json

# order confirmation mail
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from django.core.mail import EmailMultiAlternatives

# Create your views here.

# Create your views here.
def payments(request):
    body=json.loads(request.body)
    if body['status']!="COMPLETED":
        messages.error(request,'Payment Unsuccessful. Please try again!')
        return redirect('cart')
    
    order=Order.objects.get(user=request.user,order_number=body['orderID'],is_ordered=False)
    
    # store transaction details in payment model
    payment=Payment(
        user=request.user,
        payment_id=body['transID'],
        payment_method=body['payment_method'],
        amount_paid=body['amount_paid'],
        status=body['status']
    )
    payment.save()
    
    order.payment=payment
    order.is_ordered=True
    order.status='Completed'
    order.save()
    
    # make orderprodutcs
    cart_items=CartItem.objects.filter(user=request.user,is_active=True)
    for cart_item in cart_items:
        order_product=OrderProduct(order=order,payment=payment,user=request.user,product=cart_item.product,quantity=cart_item.quantity,product_price=cart_item.product.price,ordered=order.is_ordered)
        order_product.save()
        product_variations=list(cart_item.variations.all())
        order_product.variations.set(product_variations)
        order_product.save()

    # decrease sold product quantity
    for cart_item in cart_items:
        product=cart_item.product
        product.stock-=cart_item.quantity
        if product.stock<=0:
            product.is_available=False
        product.save()
    
    
    # send order confirmation email to user
    # to_email=request.user.email
    # mail_subject='Order Confirmation'
    # message=render_to_string('orders/order_confirmation_email.html',{
    #         'user':request.user,
    #         'order':order,
    #         'cart_items':cart_items,
    #     })
    
    # send_email = EmailMultiAlternatives(
    #     subject=mail_subject,
    #     body="Your order is confirmed.",  # fallback text
    #     to=[to_email],
    # )
    # send_email.attach_alternative(message, "text/html")
    # send_email.send()
    
    # delete cartitems
    cart_items.delete()
    
    # send order number and transactionID back to sendData method via response
    data={
        'order_number':order.order_number,
        'transID':payment.payment_id,
    }
    
    return JsonResponse(data)

def place_order(request,total=0,quantity=0):
    current_user=request.user
    cart_items=CartItem.objects.filter(user=current_user)
    items_count=cart_items.count()
    
    if items_count<=0:
        return redirect('cart')
    
    grand_total=0
    tax=0
    for cart_item in cart_items:
        total+=(cart_item.quantity*cart_item.product.price)
        quantity+=cart_item.quantity
        tax=(2*total/100)
        
    grand_total=total+tax
    
    if request.method=='POST':
        form=OrderForm(request.POST)
        
        if form.is_valid():
            data=Order()
            data.user=current_user
            data.first_name=form.cleaned_data['first_name']
            data.last_name=form.cleaned_data['last_name']
            data.phone=form.cleaned_data['phone']
            data.email=form.cleaned_data['email']
            data.city=form.cleaned_data['city']
            data.state=form.cleaned_data['state']
            data.country=form.cleaned_data['country']
            data.address_line_1=form.cleaned_data['address_line_1']
            data.address_line_2=form.cleaned_data['address_line_2']
            data.order_note=form.cleaned_data['order_note']

            data.order_total=grand_total
            data.tax=tax
            data.ip=request.META.get('REMOTE_ADDR')
            data.save()
            # generate orderID

            current_date = datetime.date.today().strftime("%Y%m%d")
            orderID=current_date+str(data.id)
            data.order_number=orderID
            data.save()

            order=Order.objects.get(user=current_user,is_ordered=False,order_number=orderID)
            context={
                'order':order,
                'total':total,
                'tax':tax,
                'grand_total':grand_total,
                'cart_items':cart_items,
            }
            return render(request,'orders/payments.html',context)
        return redirect('checkout')
            
def order_complete(request):
    if request.method=="GET":
        payment_id=request.GET['payment_id']
        order_number=request.GET['order_number']
        
        payment=Payment.objects.get(user=request.user,payment_id=payment_id)
        order=Order.objects.get(user=request.user,order_number=order_number,payment=payment,is_ordered=True)
        
        order_products=OrderProduct.objects.filter(order=order,payment=payment)
        
        context={
            'payment':payment,
            'order':order,
            'order_products':order_products,
        }
    return render(request,'orders/order_complete.html',context)