from django import forms 
from django.db import models

from .models import HourlyWage

class HourlyWageForm(forms.ModelForm):
    class Meta:
        model = HourlyWage
        fields = [
            'wage1',
            # 'wage2',
            'month',
        ]
