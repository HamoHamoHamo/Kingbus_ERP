from django import forms 
from django.db import models

from .models import DispatchOrder, DispatchConsumer, DispatchRoute, DispatchInfo

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
            'first_departure_date',
            ]
        test = forms.CharField()
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)

            self.fields['title'].widget.attrs.update ({'class': 'something'})
            

'''class OrderForm(forms.Form):
    class Meta:
        consumer = forms.CharField()
        bus_cnt = forms.IntegerField()
        price = forms.IntegerField()
        kinds = forms.CharField()
        purpose = forms.CharField()
        bus_type = forms.CharField()
        requirements = forms.CharField()
        people_num = forms.IntegerField()
        pay_type = forms.CharField()
        first_departure_date = forms.DateTimeField()

    def __init(self, * args, **kwargs):
            super().__init__(*args, **kwargs)
        '''