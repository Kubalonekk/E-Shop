import django_filters
from .models import *
from django_filters import DateFilter, CharFilter, BooleanFilter, ChoiceFilter, NumberFilter
from django import forms
from django.db.models import Q


class DateInput(forms.DateInput):
    input_type = 'date'


SHIPMNET_STATUS_CHOICES = (
    ('Do wysłania', 'Do wysłania'),
    ('Wysłana', 'Wysłana'),
    ('Dostarczona', 'Dostarczona'),
)


class ItemFilter(django_filters.FilterSet):
    title = CharFilter(field_name="title",
                       lookup_expr="icontains", label="Nazwa przedmiotu")
    price__gte = NumberFilter(
        field_name='price', lookup_expr='gte', label="Cena od")
    price__lte = NumberFilter(
        field_name='price', lookup_expr='lte', label="Cena do:")

    class Meta:
        model = Item
        exclude = ['description', 'slug']


class OrderFilter(django_filters.FilterSet):
    start_date = DateFilter(field_name="completion_date", lookup_expr='gte',
                            label="Ukończone od:", widget=DateInput(attrs={'type': 'date'}))
    end_date = DateFilter(field_name="completion_date", lookup_expr='lte',
                          label="Ukończone do:", widget=DateInput(attrs={'type': 'date'}))
    order_id = CharFilter(field_name="transaction_id",
                          lookup_expr="icontains", label="Numer zamówienia")
    customer = CharFilter(method="my_custom_filter", label="Klient")
    status = BooleanFilter(field_name="complete",
                           label="Płatność zakończona")
    shipment_status = ChoiceFilter(
        choices=SHIPMNET_STATUS_CHOICES, label="Status wysyłki",)

    class Meta:
        model = Order
        fields = '__all__'
        exclude = ['payment_in_progress', 'date_ordered', 'address']

    def my_custom_filter(self, queryset, name, value):
        return queryset.filter(
            Q(customer__device__icontains=value) |
            Q(customer__full_name__icontains=value)
        )
