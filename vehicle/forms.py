from django import forms
from . import models


class VehicleForm(forms.ModelForm):
    class Meta:
        model = models.Vehicle#, models.Vehicle_insurance, models.Vehicle_document
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
            'use',
            'passenger_num',
            'check_date',
            'expiration_date',
        ]

# class VehicleInsuranceForm(forms.ModelForm):
#     class Meta:
#         model = models.VehicleInsurance#, models.Vehicle_insurance, models.Vehicle_document
#         fields = [
#             'insurance_date',
#             'insurance_price',
#             'insurance_comp',
#             'expiration_date',
#         ]
#         widgets = {
#             'insurance_date': forms.DateInput(format='%Y-%m-%d', attrs={'class':'datefield'}),
#             'expiration_date': forms.DateInput(format='%Y-%m-%d', attrs={'class':'datefield'}),
#         }


# class VehicleDocumentForm(forms.ModelForm):
#     class Meta:
#         model = models.VehicleDocument
#         fields = '__all__'
