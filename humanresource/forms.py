from django import forms 
from django.db import models

from .models import Member, MemberDocument, HR

class MemberForm(forms.ModelForm):
    class Meta:
        model = Member
        fields = '__all__'

        widgets = {
            'entering_date': forms.DateTimeInput(format='%Y-%m-%d', attrs={'class':'datefield'}),
            'resignation_date': forms.DateTimeInput(format='%Y-%m-%d', attrs={'class':'datefield'}),
        }


class HRForm(forms.ModelForm):
    class Meta:
        model = HR
        fields = [
            'hr_type',
            'reason',
            'start_date',
            'finish_date',
        ]
        widgets = {
            'start_date': forms.DateTimeInput(format='%Y-%m-%d %H:%M', attrs={'class':'datetimefield'}),
            'finish_date': forms.DateTimeInput(format='%Y-%m-%d %H:%M', attrs={'class':'datetimefield'}),
        }