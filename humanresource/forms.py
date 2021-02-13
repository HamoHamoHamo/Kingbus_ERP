from django import forms 
from django.db import models

from .models import Member, MemberDocument, HR

class MemberForm(forms.ModelForm):
    class Meta:
        model = Member
        fields = '__all__'


class HRForm(forms.ModelForm):
    class Meta:
        model = HR
        fields = [
            'member_id',
            'hr_type',
            'reason',
            'date',
        ]
        widgets = {
            'date': forms.DateTimeInput(attrs={'type': 'date'}),
        }