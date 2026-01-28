from django.db import models
from django.urls import reverse
# Create your models here
class Category(models.Model):
    category_name=models.CharField(max_length=50,unique=True)
    slug=models.SlugField(max_length=100)
    category_description=models.TextField(max_length=255,blank=True)
    category_image=models.ImageField(upload_to='photos/category')
    
    class Meta:
        verbose_name='categroy'
        verbose_name_plural='categories'
    
    def get_link(self):
        return reverse('products_by_category',args=[self.slug])
    def __str__(self):
        return self.category_name
    
    
    