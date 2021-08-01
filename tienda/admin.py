from django.contrib import admin
from .models import Product, ProductGallery, Variation, ReviewRating
import admin_thumbnails
from import_export import resources
from import_export.admin import ImportExportModelAdmin

@admin_thumbnails.thumbnail('image')
class ProductGalleryInline(admin.TabularInline):
    model = ProductGallery
    extra = 1



class ProductResource(resources.ModelResource):
    fields=('product_name', 'price', 'stock', 'category','modified_date', 'is_available')
    
    class Meta:
        model = Product
    

class ProductAdmin(ImportExportModelAdmin):
    resource_class = ProductResource
    list_display = ('product_name', 'price', 'stock', 'category','modified_date', 'is_available')  # visible en base de productos
    list_filter = ('product_name', 'category')
    prepopulated_fields = {'slug': ('product_name',)}
    inlines = [ProductGalleryInline]


class VariationAdmin(admin.ModelAdmin):
    list_display = ('product', 'variation_category', 'variation_value', 'is_active')
    list_editable = ('is_active',)
    list_filter = ('product', 'variation_category', 'variation_value', 'is_active')
    
admin.site.register(Product, ProductAdmin)
admin.site.register(Variation, VariationAdmin )
admin.site.register(ReviewRating)
admin.site.register(ProductGallery)