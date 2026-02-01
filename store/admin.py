from django.contrib import admin
from .models import Product,Variation,reviewRating
# Register your models here.
class ProductAdmin(admin.ModelAdmin):
    prepopulated_fields={'slug':('product_name',)}
    list_display=('product_name','price','stock','category','is_available')
    list_editable=('stock',)
    
class variationAdmin(admin.ModelAdmin):
    list_display=('product','variation_category','variation_value')
admin.site.register(Product,ProductAdmin)
admin.site.register(Variation,variationAdmin)
admin.site.register(reviewRating)

