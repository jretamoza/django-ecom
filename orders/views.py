from carts.models import CartItem
from django.http.response import HttpResponse, JsonResponse
from django.shortcuts import redirect, render
from django.urls import reverse
from carts.models import CartItem
from .forms import OrderForm
from .models import Order, OrderProduct, Payment, Product
import datetime
import mercadopago
import json
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from decouple import config
# Create your views here.

def payments(request):
    body = json.loads(request.body)
    order = Order.objects.get(user=request.user, is_ordered=False, order_number=body['orderId'])
    
    # guardamos los datos de las transacciones en la DB de pagos
    payment = Payment(
        user = request.user,
        payment_id = body['email'],
        payment_method = body['payment_method'],
        amount_paid = order.order_total,
        status = body['status'],
    )
    payment.save()
    
    order.payment = payment
    order.is_ordered = True
    order.save()
    
    # Manejo la base de ordenes de productos
    cart_items = CartItem.objects.filter(user=request.user)
    
    for item in cart_items:
        orderproduct = OrderProduct()
        orderproduct.order_id = order.id
        orderproduct.payment = payment
        orderproduct.user_id = request.user.id
        orderproduct.product_id = item.product_id
        orderproduct.quantity = item.quantity
        orderproduct.product_price = item.product.price
        orderproduct.ordered = True
        orderproduct.save()
    
        cart_item = CartItem.objects.get(id=item.id)
        product_variation = cart_item.variations.all()
        orderproduct = OrderProduct.objects.get(id=orderproduct.id)
        orderproduct.variations.set(product_variation)
        orderproduct.save()
        
        # Reduzco stock
        product = Product.objects.get(id=item.product_id)
        product.stock -= item.quantity
        product.save()
    
    # Limpiar el carrito
    CartItem.objects.filter(user=request.user).delete()
    
    
    # Enviar la orden por Email al cliente 
    mail_subject = 'Orden recibida, muchas gracias!' 
    message = render_to_string('orders/order_email.html',{
                'user' : request.user,
                'order': order,
            })
    to_email = request.user.email
    send_email = EmailMessage(mail_subject, message, to=[to_email])
    send_email.send()
    
    
    # Enviar numero de orden y numero de la transaccion a la web 
    info = {
        'order_number': order.order_number,
        'payment_id': order.order_number, 
    }
    
    return JsonResponse(info)

def place_order(request, total=0, quantity=0):
    current_user = request.user
    
    # Si el carrito esta vacío lo redireccionamos al shopping
    cart_items = CartItem.objects.filter(user=current_user)
    cart_count = cart_items.count()
    if cart_count <= 0:
        return redirect('tienda')
    
    
    grand_total = 0
    tax = 0
    for cart_item in cart_items:
        total += (cart_item.product.price * cart_item.quantity)
        quantity += cart_item.quantity
        
    tax = (0 * total)/100 #porcentaje de impuestos que se aplican sobre el producto 
    grand_total = total + tax
    
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            data = Order()
            data.user = current_user
            data.first_name = form.cleaned_data['first_name']
            data.last_name = form.cleaned_data['last_name']
            data.phone = form.cleaned_data['phone']
            data.email = form.cleaned_data['email']
            data.address_line_1 = form.cleaned_data['address_line_1']
            data.address_line_2 = form.cleaned_data['address_line_2']
            data.country = form.cleaned_data['country']
            data.state = form.cleaned_data['state']
            data.city = form.cleaned_data['city']
            data.order_note = form.cleaned_data['order_note']
            data.order_total = grand_total
            data.tax = tax
            data.ip = request.META.get('REMOTE_ADDR')
            data.save()
            # Numero de orden
            yr = int(datetime.date.today().strftime('%Y'))
            dt = int(datetime.date.today().strftime('%d'))
            mt = int(datetime.date.today().strftime('%m'))
            d = datetime.date(yr, mt, dt)
            current_date = d.strftime("%Y%m%d")
            order_number = current_date + str(data.id)
            data.order_number = order_number
            data.save()
            
            order = Order.objects.get(user=current_user, is_ordered=False, order_number=order_number)
            pedido_identificacion = 'Pedido para: ' + form.cleaned_data['first_name'] + ' ' + form.cleaned_data['last_name'] 
            # MP - CONFIGS
            sdk = mercadopago.SDK(config('MERCADOPAGO_ACCESS_KEY'))
            preference_data = {
                                "items": [
                                    {
                                        "title": pedido_identificacion,
                                        "quantity": 1,
                                        "unit_price": grand_total,
                                    }
                                ],
                                "payer": {
                                    "name": form.cleaned_data['first_name'],
                                    "surname": form.cleaned_data['last_name'],
                                    "email": form.cleaned_data['email'],
                                    "phone": {
                                        "number": form.cleaned_data['phone'],
                                    },
                                    "address": {
                                        "street_name": form.cleaned_data['address_line_1'],
                                        "street_number": form.cleaned_data['address_line_2'],
                                    }
                                },
                                # "back_urls": {
                                #     "success": "https://www.success.com",
                                #     "failure": "http://www.failure.com",
                                #     "pending": "http://www.pending.com"
                                # },
                                # "auto_return": "approved",
                                }
            

            preference_response = sdk.preference().create(preference_data)
            preference = preference_response["response"]
            # MP - CONFIGS
            
            context = {
                'order' : order,
                'cart_items': cart_items,
                'total' : total,
                'tax' : tax, 
                'grand_total' : grand_total,
                'preference_id' : preference.get('id'),
                'MERCADOPAGO_PUCLIC_KEY':config('MERCADOPAGO_PUCLIC_KEY'),
            }
            return render(request, 'orders/payments.html', context) # pasamos el context para que los datos viajen a la pagina
        
        else:
            return redirect('checkout')
        
        
def order_complete(request):
    order_number = request.GET.get('order_number')
    transaction_id = request.GET.get('payment_id')
    
    try: 
        order = Order.objects.get(order_number=order_number, is_ordered=True)
        ordered_products = OrderProduct.objects.filter(order_id=order.id)
        
        sub_total = 0 
        
        for i in ordered_products:
            sub_total += i.product_price * i.quantity
        
        context = {
            'order': order,
            'ordered_products': ordered_products,
            'order_number': order.order_number,
            'transaction_id': transaction_id,
            'sub_total':sub_total,   
        }
        return render(request, 'orders/order_complete.html', context)
    
    except (Payment.DoesNotExist, Order.DoesNotExist):
        return redirect('home')
    
    

