from django.urls import path
from . import views
urlpatterns=[
    path('',views.store,name='store'),
    path('<slug:slug>/',views.store,name='products_by_category'),
    path('product/<slug:slug>/',views.product_detail,name='product_detail'),
]