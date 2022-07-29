from django import forms 
from django.db import models

from .models import Member

class MemberForm(forms.ModelForm):
    class Meta:
        model = Member
        fields = [
            'name',
            'role',
            'birthdate',
            'address',
            'phone_num',
            'entering_date',
            'license_number',
        ]

# class HRForm(forms.ModelForm):
#     class Meta:
#         model = HR
#         fields = [
#             'hr_type',
#             'reason',
#             'start_date',
#             'end_date',
#         ]
        