from django.db.models.aggregates import Count
from categorias.models import Categoria
from django.db import models
from django.urls import reverse
from accounts.models import Account
from django.db.models import Avg

class Product(models.Model):
    product_name        = models.CharField(max_length=200, unique=True)
    slug                = models.SlugField(max_length=200, unique=True)
    description         = models.TextField(max_length=500, blank=True)
    price               = models.IntegerField()
    images              = models.ImageField(upload_to='photos/products')
    stock               = models.IntegerField()
    is_available        = models.BooleanField(default=True)
    category            = models.ForeignKey(Categoria, on_delete=models.CASCADE) # va a ser la clave primaria
    created_date        = models.DateTimeField(auto_now_add=True)
    modified_date       = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'producto'
        verbose_name_plural = 'productos'
        
    def get_url(self):
        return reverse('products_detail', args=[self.category.slug, self.slug])
        
    def __str__(self):
        return self.product_name
    
    def averageReview(self):
        reviews = ReviewRating.objects.filter(product=self, status=True).aggregate(average=Avg('rating'))
        avg = 0
        
        if reviews['average'] is not None:
            avg = float(reviews['average'])
        return avg
            
    def countReview(self):
        reviews = ReviewRating.objects.filter(product=self, status=True).aggregate(count=Count('id'))
        count = 0
        
        if reviews['count'] is not None:
            count = int(reviews['count'])
        return count
        
        
                
class VariationManager(models.Manager):
    def colors(self):
        return super(VariationManager, self).filter(variation_category='color', is_active=True)
    
    def sizes(self):
        return super(VariationManager, self).filter(variation_category='tamaño', is_active=True)
        


# Categorias dinamicas --------------
variation_category_choice = (
    ('color', 'color'),
    ('tamaño', 'tamaño'),
)   
# ----------------------------------- 


class Variation(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    variation_category = models.CharField(max_length=100, choices=variation_category_choice)
    variation_value = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)
    created_date = models.DateTimeField(auto_now=True)
    
    objects = VariationManager()
    
    class Meta:
        verbose_name = 'variacion'
        verbose_name_plural = 'variaciones'
        
    def __str__(self):
        return self.variation_value
    
class ReviewRating(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    user = models.ForeignKey(Account, on_delete=models.CASCADE)
    subject = models.CharField(max_length=100, blank=True)
    review = models.TextField(max_length=500, blank=True)
    rating = models.FloatField()
    ip = models.CharField(max_length=20, blank=True)
    status = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = 'Reseña/Rating'
        verbose_name_plural = 'Reseñas/Ratings'
        
    def __str__(self):
        return self.subject


class ProductGallery(models.Model):
    product = models.ForeignKey(Product, default=None, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='store/products', max_length=255)
    
    class Meta:
        verbose_name = 'Galería Producto'
        verbose_name_plural = 'Galerías Productos'
    
    def __str__(self):
        return self.product.product_name