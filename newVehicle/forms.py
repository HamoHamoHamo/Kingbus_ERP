from django import forms
from . import models
from .models import Vehicle, Member, Maintenance

class MaintenanceForm(forms.ModelForm):
    class Meta:
        model = Maintenance
        fields = ['type', 'work_date', 'content', 'cost']

class VehicleForm(forms.ModelForm):
    class Meta:
        model = models.Vehicle
        fields = [
            'vehicle_number_front',
            'vehicle_number_back',
            'garage',
            'maker',
            'make_year',
            'vehicle_name',
            'driver',
            'vehicle_serial',
            'passenger_capacity',
            'type',
            'model_year',
            'fuel_type',
            'registration_date',
            'in_use',
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
            'cold',
            'sing',
            'usb',
            'hot',
            'tv'
        ]
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # `role`이 '운전원', '팀장', '용역'인 멤버만 가져오기
        self.fields['driver'].queryset = Member.objects.filter(role__in=['운전원', '팀장', '용역'])
# class MaintenanceForm(forms.ModelForm):
#     class Meta:
#         model = models.Maintenance
#         fields = [
#             'maintenance_type',
#             'work_date',
#             'work_detail',
#             'work_price'
#         ]
    
    
    
    
    
    
    
    
    
    
    # class Meta:
    #     model = Vehicle
    #     fields = ['vehicle_number_front', 'vehicle_number_back', 'maker', 'vehicle_name', 'driver', 'vehicle_serial', 'passenger_capacity', 'model_year']

    # def clean(self):
    #     cleaned_data = super().clean()
    #     vehicle_number_front = cleaned_data.get('vehicle_number_front')
    #     vehicle_number_back = cleaned_data.get('vehicle_number_back')

    #     # 차량번호 필드들이 비어있을 때 오류 메시지 하나로 처리
    #     if not vehicle_number_front or not vehicle_number_back:
    #         raise forms.ValidationError('차량 번호는 필수 사항입니다. 앞/뒤 번호를 모두 입력하세요.')

    #     return cleaned_data
