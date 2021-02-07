from django import forms 
from django.db import models

from .models import DispatchOrder, DispatchConsumer, DispatchRoute, DispatchConnect

class OrderForm(forms.ModelForm):
    class Meta:
        model = DispatchOrder
        fields = [ 
            'bus_cnt', 
            'price', 
            'kinds',
            'purpose',
            'bus_type',
            'requirements',
            'people_num',
            'pay_type',
            ]
        '''
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)

            self.fields['kinds'].widget.attrs.update ({'class': 'something'})
        '''

'''
class OrderForm(forms.Form):
    bus_cnt = forms.IntegerField(label="버스대수")
    price = forms.IntegerField(label="가격")
    kinds = forms.CharField(label="왕복or편도")
    purpose = forms.CharField(label="용도")
    bus_type = forms.CharField(label="버스종류")
    requirements = forms.CharField(label="요구사항")
    people_num = forms.IntegerField(label="탑승인원")
    pay_type = forms.CharField(label="카드or현금")


    def save(self, commit=True):
        self.instance = DispatchOrder(**self.cleaned_data)
        if commit:
            self.instance.save()
        return self.instance
'''
class ConsumerForm(forms.ModelForm):
    class Meta:
        model = DispatchConsumer
        fields = '__all__'