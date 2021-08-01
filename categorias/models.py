from django.db import models
from django.urls import reverse

# Create your models here.

class Categoria(models.Model):
    category_name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(max_length=100, unique=True)
    description = models.TextField(max_length=255, blank=True) # es opcional entonces puede estar en blanco
    category_image = models.ImageField(upload_to='photos/categories', blank=True)
    
    class Meta:
        verbose_name = 'categoría'
        verbose_name_plural = 'categorías'
        
    def get_url(self):
        return reverse('products_by_category', args=[self.slug])
            
    def __str__(self):
       return self.category_name