from django import forms 
from django.db import models

from .models import AdditionalSalary, Income, AdditionalCollect

class AdditionalForm(forms.ModelForm):
    class Meta:
        model = AdditionalSalary
        fields = [
            'date',
            'price',
            'remark',
        ]

class AdditionalCollectForm(forms.ModelForm):
    class Meta:
        model = AdditionalCollect
        fields = [
            'category',
            'value',
            'VAT',
            'note',
        ]

class IncomeForm(forms.ModelForm):
    class Meta:
        model = Income
        fields = [
            'date',
            'depositor',
            'payment_method',
            'bank',
            'acc_income',
        ]

