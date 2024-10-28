from django import forms
from . import models


class VehicleForm(forms.ModelForm):
    class Meta:
        model = models.Vehicle
        fields = [
            'vehicle_num0',
            'vehicle_num',
            'vehicle_id',
            'motor_type',
            'rated_output',
            'vehicle_type',
            'maker',
            'model_year',
            'release_date',
            'driver',
            'use',
            'passenger_num',
            'check_date',
            'type',
            'garage',
            'remark',

            'vehicle_price',
            'depreciation_month',
            'number_price',
            'depreciation_year',
            'insurance_pay_date',
            'insurance_price',
            'monthly_installment',
            'remaining_installment_amount',

            'led',
            'fridge',
            'sing',
            'usb',
            'water_heater',
            'tv',
        ]

class MaintenanceForm(forms.ModelForm):
    class Meta:
        model = models.Maintenance
        exclude = ['creator']