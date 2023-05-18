from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.forms import ModelForm
from .models import *
from phonenumber_field.modelfields import PhoneNumberField
from django.core.validators import RegexValidator
from django.contrib.admin.widgets import AdminDateWidget
from django.forms.fields import DateField


class UserRegisterForm(UserCreationForm):
    first_name = forms.CharField(max_length=50, label="Imię")
    last_name = forms.CharField(max_length=50, label="Nazwisko")
    phone_regex = RegexValidator(
        regex=r'(?<!\w)(\(?(\+|00)?48\)?)?[ -]?\d{3}[ -]?\d{3}[ -]?\d{3}(?!\w)', message="Wprowadź numer w formacie 123456789")
    phone = forms.CharField(
        validators=[phone_regex], max_length=17, label="Numer telefonu",)

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name',
                  'last_name', 'password1', 'password2',]


class LoginForm(forms.Form):
    username = forms.CharField(max_length=63, label="Nazwa użytkownika",)
    password = forms.CharField(
        max_length=63, widget=forms.PasswordInput, label="Hasło",)


class DeliveryAddressForm(forms.ModelForm):
    email = forms.EmailField()
    name = forms.CharField(max_length=50, label="Imię")
    last_name = forms.CharField(max_length=50, label="Nazwisko")
    street_address = forms.CharField(
        max_length=50, label="Ulica i numer budynku")
    city = forms.CharField(max_length=50, label="Miasto")
    postcode = forms.CharField(max_length=50, label="Kod pocztowy")
    # phone_regex = RegexValidator(regex=r'(?<!\w)(\(?(\+|00)?48\)?)?[ -]?\d{3}[ -]?\d{3}[ -]?\d{3}(?!\w)', message="Wprowadź numer w formacie 123456789")
    # phone = forms.CharField(validators=[phone_regex], max_length=17, label="Numer telefonu",)
    # postcode_regex = RegexValidator(regex=r'^[0-9]{2}-[0-9]{3}', message="Wprowadź kod pocztowy w formacie 00-000")
    # phone = forms.CharField(validators=[phone_regex], max_length=17, label="Numer telefonu",)
    postcode = forms.CharField(max_length=6)

    class Meta:
        model = AddressInformation
        exclude = ['customer']

