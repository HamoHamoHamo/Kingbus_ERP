from django import forms 
from django.db import models

from .models import Member, MemberDocument, HR

class MemberForm(forms.ModelForm):
    class Meta:
        model = Member
        fields = [
            'name',
            'role',
            'person_id1',
            'person_id2',
            'address',
            'phone_num',
            'entering_date',
            'resignation_date',
        ]

        widgets = {
            'entering_date': forms.DateTimeInput(format='%Y-%m-%d', attrs={'class':'datefield'}),
            'resignation_date': forms.DateTimeInput(format='%Y-%m-%d', attrs={'class':'datefield'}),
        }

class MemberEditForm(forms.ModelForm):
    class Meta:
        model = Member
        fields = '__all__'

class HRForm(forms.ModelForm):
    class Meta:
        model = HR
        fields = [
            'hr_type',
            'reason',
            'start_date',
            'finish_date',
        ]
        