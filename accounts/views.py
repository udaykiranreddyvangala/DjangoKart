from django.shortcuts import render,redirect
from django.http import HttpResponse
from .forms import RegisterForm,userForm,userProfileForm
from .models import Account,UserProfile
from django.contrib import messages
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from cart.models import Cart,CartItem
from cart.views import _cart_id
import requests
from orders.models import Order,OrderProduct

# verification mail
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_decode,urlsafe_base64_encode
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMessage
# Create your views here.
def register(request):
    if request.user.is_authenticated:
        return redirect('home')
    if request.method=='POST':
        form=RegisterForm(request.POST)
        
        if form.is_valid():
            first_name=form.cleaned_data['first_name']
            last_name=form.cleaned_data['last_name']
            email=form.cleaned_data['email']
            username=form.cleaned_data['username']
            phone_number=form.cleaned_data['phone_number']
            password=form.cleaned_data['password']
            
            user=Account.objects.create_user(
                first_name=first_name,
                last_name=last_name,
                email=email,
                username=username,
                password=password
            )
            user.phone_number=phone_number
            user.save()
            
            # user profile creation
            user_profile=UserProfile(user=user)
            user_profile.profile_picture='default/defaul-user.png'
            user_profile.save()
            
            #User activation
            domain=get_current_site(request)
            mail_subject='Please activate your account'
            message=render_to_string('accounts/account_verification_email.html',
                                    {
                                        'user':user,
                                        'domain':domain,
                                        'uid':urlsafe_base64_encode(force_bytes(user.pk)),
                                        'token':default_token_generator.make_token(user),
                                    })
            to_email=email
            send_email=EmailMessage(mail_subject,message,to=[to_email])
            send_email.send()
            # messages.success(request,'Registration Successful!')
            return redirect(
                reverse('login') + f'?command=verification&email={email}'
            )
    else:    
        form=RegisterForm()
    context={
        'form':form,
    }
    return render(request,'accounts/register.html',context)

def login(request):
    if request.user.is_authenticated:
        return redirect('home')
    if request.method=='POST':
        email=request.POST.get('email')
        password=request.POST.get('password')
        
        user=auth.authenticate(email=email,password=password)
        
        if user is not None:
            try:
                cart=Cart.objects.get(cart_id=_cart_id(request))
                cart_items=CartItem.objects.filter(cart=cart)
                auth.login(request,user)
                for cart_item in cart_items:
                    # cart_item.user=user
                    # cart_item.save()
                    product=cart_item.product
                    product_variations=list(cart_item.variations.all())
                    print(product_variations)
                    existing_cart_items=CartItem.objects.filter(user=request.user,product=product)
                    print(existing_cart_items)
                    existing_variations=[]
                    cart_item_id=[]
                    for existing_cart_item in existing_cart_items:
                        curr_variations=list(existing_cart_item.variations.all())
                        existing_variations.append(curr_variations)
                        cart_item_id.append(existing_cart_item.id)
                        
                    if product_variations in existing_variations:
                        index=existing_variations.index(product_variations)
                        existing_cart_item_id=cart_item_id[index]
                        existing_cart_item=CartItem.objects.get(id=existing_cart_item_id)
                        existing_cart_item.quantity+=cart_item.quantity
                        existing_cart_item.save()
                        cart_item.delete()
                    else:
                        cart_item.user=user
                        cart_item.save()
                    
            except Cart.DoesNotExist:
                pass
            auth.login(request,user)
            messages.success(request,'Login Successful')
            url=request.META.get('HTTP_REFERER')
            try:
                query=requests.utils.urlparse(url).query
                params = dict(x.split('=') for x in query.split('&'))
                if 'next' in params:
                    nextPage = params['next' ]
                    return redirect(nextPage)
            except:     
                return redirect('dashboard')
        else:
            messages.error(request,"Invalid login credentials")
            return redirect('login')
    return render(request,'accounts/login.html')

@login_required(login_url='login')
def logout(request):
    auth.logout(request)
    messages.success(request,'Logout Successful')
    return redirect('login')

def activate(request,uidb64,token):
    try:
        uid=urlsafe_base64_decode(uidb64).decode()
        user=Account._default_manager.get(pk=uid)
        
    except(ValueError,TypeError,OverflowError,Account.DoesNotExist):
        user=None
        
    if user is not None and default_token_generator.check_token(user,token):
        user.is_active=True
        user.save()
        messages.success(request,'Congratulations! Your account is acivated ') 
        return redirect('login')
    else:
        messages.error('request','Invalid activation link')
        return redirect('register')

@login_required(login_url='login')
def dashboard(request):
    user=request.user
    try:
        userprofile=UserProfile.objects.get(user=user)
    except:
        if user.is_admin:
            user_profile=UserProfile(user=user)
            user_profile.profile_picture='default/defaul-user.png'
            user_profile.save()
            userprofile=user_profile
        
    orders_count=Order.objects.filter(user=user,is_ordered=True).count()
    context={
        'orders_count':orders_count,
        'userprofile':userprofile,
    }
    return render(request,'accounts/dashboard.html',context)
@login_required(login_url='login')
def change_password(request):
    user=Account.objects.get(email__exact=request.user.email)
    if request.method=='POST':
        current_password=request.POST['current_password']
        new_password=request.POST['new_password']
        confirm_password=request.POST['confirm_password']
        
        if new_password==confirm_password:
            is_correct=user.check_password(current_password)
            if is_correct:
                user.set_password(new_password)
                user.save()
                messages.success(request,'Password updation successful')
                auth.logout(request)
                return redirect('change_password')
            else:
                messages.error(request,'Incorrect current password')
                return redirect('change_password')
        else:
            messages.error(request,'Passwords do not match')
            return redirect('change_password')
    return render(request,'accounts/change_password.html')
@login_required(login_url='login')
def edit_profile(request):
    
    user_profile=UserProfile.objects.get(user=request.user)
    if request.method=='POST':
        user_form=userForm(request.POST,instance=request.user)
        profile_form=userProfileForm(request.POST,request.FILES,instance=user_profile)
        
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request,'User profile updation Successful!')
            return redirect('edit_profile')
    else:
        user_form=userForm(instance=request.user)
        profile_form=userProfileForm(instance=user_profile)
        
    context={
        'user_form':user_form,
        'profile_form':profile_form,
        'userprofile':user_profile,
    }
    return render(request,'accounts/edit_profile.html',context)
@login_required(login_url='login')
def my_orders(request):
    orders=Order.objects.filter(user=request.user,is_ordered=True).order_by('-created_at')
    context={
        'orders':orders,
    }
    return render(request,'accounts/my_orders.html',context)

@login_required(login_url='login')
def order_detail(request,order_number):
    order=Order.objects.get(order_number=order_number)
    order_products=OrderProduct.objects.filter(order=order)
    context={
        'order':order,
        'order_detail':order_products,
    }
    
    return render(request,'accounts/order_detail.html',context)
    
    
def forgot_password(request):
    if request.method=='POST':
        email=request.POST['email']
        
        if Account.objects.filter(email=email).exists():
            try:
                user=Account.objects.get(email__exact=email)
                
                # email
                domain=get_current_site(request)
                mail_subject='Reset Your Password'
                message=render_to_string('accounts/reset_password_email.html',
                                        {
                                            'user':user,
                                            'domain':domain,
                                            'uid':urlsafe_base64_encode(force_bytes(user.pk)),
                                            'token':default_token_generator.make_token(user),
                                        })
                to_email=email
                send_email=EmailMessage(mail_subject,message,to=[to_email])
                send_email.send()
                messages.success(request,'Password reset email has been sent to your email address!')
                return redirect('login')
            except Account.DoesNotExist:
                pass
        else:
            messages.error(request,'Account does not exist!')
            return redirect('forgot_password')
    return render(request,'accounts/forgot_password.html')

def reset_password(request,uidb64,token):
    try:
        uid=urlsafe_base64_decode(uidb64).decode()
        user=Account._default_manager.get(pk=uid)
    
    except(ValueError,TypeError,OverflowError,Account.DoesNotExist):
        user=None
    
    if user is not None and default_token_generator.check_token(user,token):
        request.session['uid']=user.id
        messages.success(request,'Please reset password')
        return redirect('reset_password_validate')
    else:
        messages.error('request','Invalid reset link')
        return redirect('login')


def reset_password_validate(request):
    if request.method=='POST':
        password=request.POST['password']
        confirm_password=request.POST['confirm_password']
        
        if password==confirm_password:
            uid=request.session.get('uid')
            user=Account._default_manager.get(pk=uid)
            
            user.set_password(password)
            user.save()
            messages.success(request,'Password reset successful!')
            return redirect('login')
        else:
            messages.error(request,'Passwords do not match!')
            return redirect('reset_password_validate')
    return render(request,'accounts/reset_password_validate.html')