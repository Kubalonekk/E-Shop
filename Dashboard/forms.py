from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.forms import ModelForm
from App.models import *
from django.core.validators import RegexValidator
from django.contrib.admin.widgets import AdminDateWidget
from django.forms.fields import DateField


class EditOrderForm(forms.ModelForm):

    class Meta:
        model = Order
        exclude = ['customer', 'date_ordered',]


class AddItemForm(forms.ModelForm):
    class Meta:
        model = Item
        exclude = ['slug']


class AddItemVariantForm(forms.ModelForm):
    class Meta:
        model = ItemVariant
        exclude = ['color']
