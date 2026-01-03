from django.contrib import admin

from .models import Category

class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields=({'slug':('category_name',)})
    list_display=('category_name',)
    search_fields=('category_name','description')

# Register your models here.
admin.site.register(Category,CategoryAdmin)
