from django import template
from App.models import Order, OrderItem, Customer
import uuid

register = template.Library()

@register.filter
def cart_item_count(request):
    try:
        customer = request.user.customer
    except:
        device = request.session.get('device')
        if request.session.get('device') is None:
            request.session['device'] = str(uuid.uuid4())
            device = request.session.get('device')              
        customer, created = Customer.objects.get_or_create(device=device)
    order, created = Order.objects.get_or_create(customer=customer, complete=False)
    order = order.get_cart_objects_quantity
    return order
       
       
