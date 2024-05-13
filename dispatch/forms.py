from django import forms 
from django.db import models

from .models import DispatchOrder, DispatchOrderConnect, DispatchRegularlyData, Station

class RegularlyDataForm(forms.ModelForm):
    class Meta:
        model = DispatchRegularlyData
        fields = [
            'references',
            'departure',
            'arrival',
            # 'departure_time',
            # 'arrival_time',
            # 'bus_type',
            # 'bus_cnt',
            # 'price',
            # 'driver_allowance',
            'number1',
            'number2',
            # 'customer',
            # 'customer_phone',
            # 'contract_start_date',
            # 'contract_end_date',
            'work_type',
            'route',
            'location',
            'detailed_route',
            'maplink',
            'use',
            'distance',
        ]

class OrderForm(forms.ModelForm):
    class Meta:
        model = DispatchOrder
        fields = [
            'operation_type',
            'references',
            'departure',
            'arrival',
            'bus_type',
            'bus_cnt',
            'contract_status',
            'customer',
            'customer_phone',
            'bill_place',
            'ticketing_info',
            'order_type',
            'operating_company',
            'reservation_company',
            'driver_lease',
            'vehicle_lease',
        ]
        
        # widgets = {
        #     'departure_date': forms.DateInput(format='%Y-%m-%d H:i', attrs={'type':'datetime-local'}),
        #     'arrival_date': forms.DateInput(format='%Y-%m-%d H:i', attrs={'type':'datetime-local'}),
        # }
        

class ConnectForm(forms.ModelForm):
    class Meta:
        model = DispatchOrderConnect
        fields = [
            'bus_id',
            'driver_id',
            'departure_date',
            'arrival_date',
        ]

class StationForm(forms.ModelForm):
    class Meta:
        model = Station
        fields = [
            'name',
            'address',
            'latitude',
            'longitude',
            'references',
        ]