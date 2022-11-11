from django import forms 
from django.db import models

from .models import AdditionalSalary, Income

class AdditionalForm(forms.ModelForm):
    class Meta:
        model = AdditionalSalary
        fields = [
            'date',
            'price',
            'remark',
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

