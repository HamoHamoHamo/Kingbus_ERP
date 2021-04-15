from django import forms 
from django.db import models

from .models import DispatchOrder, DispatchConsumer, DispatchConnect, DispatchRoute

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
            'departure_date',
            'arrival_date',
            ]

        widgets = {
            'departure_date': forms.DateInput(format='%Y-%m-%d H:i', attrs={'class':'datetimefield'}),
            'arrival_date': forms.DateInput(format='%Y-%m-%d H:i', attrs={'class':'datetimefield'}),
        }

class RouteForm(forms.ModelForm):
    class Meta:
        model = DispatchRoute
        fields = [
            'departure',
            'arrival',
            'stopover',
            'route_name',
        ]
class ConnectForm(forms.ModelForm):
    class Meta:
        model = DispatchConnect
        fields = [
            'bus_id',
            'driver_id',
        ]
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