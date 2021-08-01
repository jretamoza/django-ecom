from django import forms
from .models import Order


class OrderForm(forms.ModelForm): #Te da una replica de la db
    class Meta:
        model = Order
        fields = ['first_name', 'last_name', 'phone', 'email', 'address_line_1', 'address_line_2', 'country', 'state', 'city', 'order_note'] #vienen de models dentro de order
    