from django.contrib import admin
from .models import Product
# Register your models here.

class ProductAdmin(admin.ModelAdmin):
    prepopulated_fields=({'slug':('product_name',)})
    list_display=('product_name','category','price','is_available','stock')
    list_editable=('price','is_available','stock')

admin.site.register(Product,ProductAdmin)
