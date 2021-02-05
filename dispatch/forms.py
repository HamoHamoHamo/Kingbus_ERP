from django import forms 
from django.db import models

from .models import DispatchOrder, DispatchConsumer, DispatchRoute, DispatchInfo
'''
class OrderForm(forms.ModelForm):
    class Meta:
        model = DispatchOrder
        fields = [
            'consumer', 
            'bus_cnt', 
            'price', 
            'kinds',
            'purpose',
            'bus_type',
            'requirements',
            'people_num',
            'pay_type',
            ]
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)

            self.fields['kinds'].widget.attrs.update ({'class': 'something'})
          '''  

class OrderForm(forms.Form):
    bus_cnt = forms.IntegerField()
    price = forms.IntegerField()
    kinds = forms.CharField()
    purpose = forms.CharField()
    bus_type = forms.CharField()
    requirements = forms.CharField()
    people_num = forms.IntegerField()
    pay_type = forms.CharField()
    consumer_name = forms.CharField()
    consumer_tel = forms.IntegerField()