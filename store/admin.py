from django.contrib import admin
from .models import Product,Variation
# Register your models here.

class ProductAdmin(admin.ModelAdmin):
    prepopulated_fields=({'slug':('product_name',)})
    list_display=('product_name','category','price','is_available','stock')
    list_editable=('price','is_available','stock')
    
class VariationAdmin(admin.ModelAdmin):
    list_display=('product','variation_category','variation_value','is_active')
    list_editable=('variation_value','is_active')
    list_filter=('product','variation_category','variation_value','is_active')
    
admin.site.register(Product,ProductAdmin)
admin.site.register(Variation,VariationAdmin)
