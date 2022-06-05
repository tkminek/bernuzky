from django import forms
from .models import *
from django.forms import ModelForm


class PaymentForm(ModelForm):
    class Meta:
        model = Payment
        exclude = ['user', 'order']
        widgets = {
                "name": forms.RadioSelect(choices=PAYMENT_CHOICES),
            }


class AddressForm(ModelForm):
    class Meta:
        model = Address
        exclude = ['user', 'order']
        widgets = {
                "name": forms.TextInput(attrs={"class": "form-control", "placeholder": "Křestní jméno"}),
                "surname": forms.TextInput(attrs={"class": "form-control", "placeholder": "Přijmení"}),
                "email": forms.TextInput(attrs={"class": "form-control", "placeholder": "Kontaktní email"}),
                "city": forms.TextInput(attrs={"class": "form-control", "placeholder": "Název města"}),
                "street_address": forms.TextInput(attrs={"class": "form-control", "placeholder": "Název ulice"}),
                "street_number": forms.TextInput(attrs={"class": "form-control", "placeholder": "Číslo popisn"}),
                "zip": forms.TextInput(attrs={"class": "form-control", "placeholder": "PSČ"}),
            }
