from django.urls import path
from . import views
urlpatterns=[
    path('register/',views.register,name='register'),
    path('login/',views.login,name='login'),
    path('logout/',views.logout,name='logout'),
    path('',views.dashboard,name='dashboard'),
    path('dashboard/',views.dashboard,name='dashboard'),
    path('my_orders/',views.my_orders,name='my_orders'),
    path('order_detail/<str:order_number>',views.order_detail,name='order_detail'),
    path('edit_profile/',views.edit_profile,name='edit_profile'),
    path('change_password/',views.change_password,name='change_password'),
    
    #account activation
   path('activate/<uidb64>/<token>/',views.activate,name='activate'),
   
    #forgot,reset password functionality
    path('forgot_password/',views.forgot_password,name='forgot_password'),
    path('reset_password/<uidb64>/<token>/',views.reset_password,name='reset_password'),
    path('reset_password_validate/',views.reset_password_validate,name='reset_password_validate'),
]