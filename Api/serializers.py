from rest_framework import serializers
from App.models import *


class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
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
    get_cart_total_without_cupon = serializers.SerializerMethodField()
    get_cart_total = serializers.SerializerMethodField()
    get_cupon_value = serializers.SerializerMethodField()

    class Meta:
        model = Order
        fields = ('id', 'customer', 'address', 'date_ordered', 'complete', 'transaction_id', 'payment_in_progress',
                  'completion_date', 'get_cart_total_without_cupon', 'shipment_status', 'cupon', 'get_cart_total', 'get_cupon_value')

    def get_cart_total_without_cupon(self, object):
        return object.get_cart_total_without_cupon()

    def get_cart_total(self, object):
        return object.get_cart_total()

    def get_cupon_value(self, object):
        return object.get_cupon_value()


class OrderItemSerializer(serializers.ModelSerializer):
    get_total = serializers.SerializerMethodField()

    class Meta:
        model = OrderItem
        fields = ('item', 'order', 'quantity',
                  'date_added', 'get_total', 'item_variant')
        depth = 2

    def get_total(self, object):
        return object.get_total()


class ItemImagesSerializer(serializers.ModelSerializer):
    class Meta:
        model = ItemImages
        fields = '__all__'
        depth = 2
