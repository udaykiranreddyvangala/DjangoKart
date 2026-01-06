from django.urls import path
from .import views
urlpatterns=[
    path('',views.cart,name='cart'),
    path('add_cart/<int:product_id>/',views.add_cart,name='add_cart'),
    path('remove/<int:id>/',views.remove,name='remove'),
    path('remove_cart/<int:id>/',views.remove_cart,name='remove_cart'),
]