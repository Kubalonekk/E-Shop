import django_filters
from App.models import *
from django_filters import DateFilter, CharFilter, BooleanFilter, ChoiceFilter, NumberFilter
from django import forms
from django.db.models import Q


class DateInput(forms.DateInput):
    input_type = 'date'

class ItemFilter(django_filters.FilterSet):
    title = CharFilter(field_name="title",
                       lookup_expr="icontains")
    class Meta:
        model = Item
        fields = ['title']
        