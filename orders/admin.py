from django.contrib import admin
from .models import Payment, Order, OrderProduct

# Register your models here.

class OrderProductInline(admin.TabularInline):
    model = OrderProduct
    readonly_fields = ('payment', 'user', 'product', 'quantity','product_price','ordered')
    extra = 0
    
    
class OrderAdmin(admin.ModelAdmin):
    list_display = ['order_number', 'full_name', 'phone', 'email', 'order_total','is_ordered', 'created_at']
    list_filter = ['status', 'is_ordered', 'created_at']
    search_fields = ['order_number', 'first_name', 'last_name', 'phone', 'email', 'order_total','created_at']
    list_per_page = 20
    inlines = [OrderProductInline]

class PaymentAdmin(admin.ModelAdmin):
    list_display = ['user','amount_paid','created_at']
    list_filter = ['created_at']
    
admin.site.register(Payment, PaymentAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(OrderProduct)
