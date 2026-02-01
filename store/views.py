from django.shortcuts import render,redirect
from .models import Product,reviewRating
from cart.models import Cart,CartItem
from cart.views import _cart_id
from django.core.paginator import EmptyPage,PageNotAnInteger,Paginator
from .forms import reviewRatingForm
from django.contrib import messages
from orders.models import OrderProduct
from django.db.models import Avg
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
    is_purchased=False
    order_products=OrderProduct.objects.filter(user=request.user)
    reviews=reviewRating.objects.filter(product=product,status=True)
    reviews_count=reviews.count()
    average_rating = reviews.aggregate(Avg('rating'))['rating__avg']
    if average_rating:
        product.averageReview=average_rating
        product.save()  
    
    for order_product in order_products:
        if order_product.product==product:
            is_purchased=True
            break
            
    
    in_cart=CartItem.objects.filter(cart__cart_id=_cart_id(request),product=product).exists()
    form=reviewRatingForm()
    context={
        'reviews_count':reviews_count,
        'product':product,
        'reviews':reviews,
        'in_cart':in_cart,
        'is_purchased':is_purchased,
        'form':form,
    }
    
    return render(request,'product_detail.html',context)

def submit_review(request,product_id):
   
    url=request.META['HTTP_REFERER']
    product=Product.objects.get(id=product_id)
    if request.method=='POST':
        try:
            review=reviewRating.objects.get(user=request.user,product=product)
            form=reviewRatingForm(request.POST,instance=review)
            form.save()
            messages.success(request,'Thank you.Your review has been updated successfully!')
            return redirect(url)
        except reviewRating.DoesNotExist:
            form=reviewRatingForm(request.POST)
            if form.is_valid():
                data=reviewRating()
                data.rating=form.cleaned_data['rating']
                data.subject=form.cleaned_data['subject']
                data.review=form.cleaned_data['review']
                data.user=request.user
                data.product=product
                data.ip=request.META['REMOTE_ADDR']
                data.save()
                messages.success(request,'Thank you.Your review has been submitted successfully!')
                return redirect(url)
                
            

