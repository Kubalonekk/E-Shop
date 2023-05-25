from rest_framework import serializers
from App.models import *


class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = '__all__'
        depth = 2


class ItemVariantSerializer(serializers.ModelSerializer):
    class Meta:
        model = ItemVariant
        fields = '__all__'
        depth = 2


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'
        depth = 2


class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = '__all__'


class AddressInformationSerializer(serializers.ModelSerializer):
    class Meta:
        model = AddressInformation
        fields = '__all__'


class ItemSizeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ItemSize
        fields = '__all__'


class CuponSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cupon
        fields = '__all__'


class OrderSerializer(serializers.ModelSerializer):
    cart_total_without_cupon = serializers.DecimalField(source="get_cart_total_without_cupon", max_digits=6, decimal_places=2)
    cart_total = serializers.DecimalField(source="get_cart_total", max_digits=6, decimal_places=2)
    cupon_value = serializers.DecimalField(source="get_cupon_value", max_digits=6, decimal_places=2)
    get_cart_objects_quantity = serializers.DecimalField(
        max_digits=6, decimal_places=26)

    class Meta:
        model = Order
        depth = 2
        fields = ('id', 'customer', 'address', 'date_ordered', 'complete', 'transaction_id', 'payment_in_progress',
                  'completion_date', 'cart_total_without_cupon', 'shipment_status', 'cupon', 'cart_total', 'cupon_value', 'get_cart_objects_quantity')

    def get_cart_objects_quantity(self, object):
        return object.get_cart_objects_quantity()


class OrderItemSerializer(serializers.ModelSerializer):
    total = serializers.DecimalField(source="get_total", max_digits=6, decimal_places=2)

    class Meta:
        model = OrderItem
        fields = ('id', 'item', 'order', 'quantity',
                  'date_added', 'total', 'item_variant')
        depth = 2



class ItemImagesSerializer(serializers.ModelSerializer):
    class Meta:
        model = ItemImages
        fields = '__all__'
        depth = 2
