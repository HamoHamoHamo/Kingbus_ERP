from django import forms 
from django.db import models

from .models import Outlay, Income, Collect, MonthlySalary, DailySalary




class OutlayForm(forms.ModelForm):
    class Meta:
        model = Outlay
        fields = [
            'kinds',
            'salary_id',
            #'vehicle_id',
            'brief',
            'price',
            'outlay_date',
        ]
        widgets = {
            'outlay_date': forms.DateInput(format='%Y-%m-%d', attrs={'class':'datefield', 'type':'date'}),
        }

class CollectForm(forms.ModelForm):
    class Meta:
        model = Collect
        fields = [
            'brief',
            'collect_date',
            'check',
            'remark',
        ]
        widgets = {
            'collect_date': forms.DateInput(format='%Y-%m-%d', attrs={'class':'datefield'}),
        }

class IncomeForm(forms.ModelForm):
    class Meta:
        model = Income
        fields = [
            'brief',
            'price',
            'income_date',
        ]
        widgets = {
            'income_date': forms.DateInput(format='%Y-%m-%d', attrs={'class':'datefield'}),
        }