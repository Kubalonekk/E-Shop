from django import template
from App.models import Order, OrderItem, Customer

register = template.Library()

@register.filter
def cart_item_count(request):
    try:
        customer = request.user.customer
    except:
        try:
            device = request.COOKIES['device']
            customer, created = Customer.objects.get_or_create(device=device)
        except:
            return 0
    order, created = Order.objects.get_or_create(customer=customer, complete=False)
    order = order.get_cart_objects_quantity
    return order
       
       
