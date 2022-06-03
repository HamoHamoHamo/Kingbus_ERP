from django import forms
from . import models


class VehicleDetailForm(forms.ModelForm):
    class Meta:
        model = models.Vehicle#, models.Vehicle_insurance, models.Vehicle_document
        fields = [
            'vehicle_num',
            'vehicle_id',
            'group',
            'vehicle_type',
            'maker',
            'model_year',
            'release_date',            
            'use',
            'passenger_num',
        ]

class VehicleInsuranceForm(forms.ModelForm):
    class Meta:
        model = models.VehicleInsurance#, models.Vehicle_insurance, models.Vehicle_document
        fields = [
            'insurance_date',
            'insurance_price',
            'insurance_comp',
            'expiration_date',
        ]
        widgets = {
            'insurance_date': forms.DateInput(format='%Y-%m-%d', attrs={'class':'datefield'}),
            'expiration_date': forms.DateInput(format='%Y-%m-%d', attrs={'class':'datefield'}),
        }


class VehicleDocumentForm(forms.ModelForm):
    class Meta:
        model = models.VehicleDocument
        fields = '__all__'
