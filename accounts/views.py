from django.shortcuts import render,redirect
from django.http import HttpResponse
from .forms import RegisterForm
from .models import Account
from django.contrib import messages
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.urls import reverse

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
        
        print(email,password)
        user=auth.authenticate(email=email,password=password)
        
        if user is not None:
            auth.login(request,user)
            messages.success(request,'Login Successful')
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
    return render(request,'accounts/dashboard.html')


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