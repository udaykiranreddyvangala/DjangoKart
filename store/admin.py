from django.contrib import admin
from .models import Product,Variation,reviewRating,ProductGallery
from django.utils.html import format_html
import admin_thumbnails
# Register your models here.
@admin_thumbnails.thumbnail('image')
class ProductGalleryAdmin(admin.ModelAdmin):
    # model=ProductGallery
#     def thumbnail(self,object):
#          return format_html('<img src="{}" width="30">',object.image.url)
#     thumbnail.short_description='Product Image'
    list_display=('product','image_thumbnail')
    
@admin_thumbnails.thumbnail('image')
class ProductGalleryInline(admin.TabularInline):
    list_display=('image_thumbnail',)
    model=ProductGallery
    extra=1
    
class ProductAdmin(admin.ModelAdmin):
    prepopulated_fields={'slug':('product_name',)}
    list_display=('product_name','price','stock','category','is_available')
    list_editable=('stock',)
    inlines=[ProductGalleryInline]
    
class variationAdmin(admin.ModelAdmin):
    list_display=('product','variation_category','variation_value')
    
admin.site.register(Product,ProductAdmin)
admin.site.register(Variation,variationAdmin)
admin.site.register(reviewRating)
admin.site.register(ProductGallery,ProductGalleryAdmin)

