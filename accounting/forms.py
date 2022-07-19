from django import forms 
from django.db import models

from .models import AdditionalSalary

class AdditionalForm(forms.ModelForm):
    class Meta:
        model = AdditionalSalary
        fields = [
            'date',
            'price',
            'remark',
        ]

