from django.contrib import admin
from .models import *

admin.site.register(Customer)
admin.site.register(AddressInformation)
admin.site.register(Category)
admin.site.register(Item)
admin.site.register(ItemImages)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(ItemColor)
admin.site.register(ItemSize)
admin.site.register(ItemVariant)
admin.site.register(Cupon)