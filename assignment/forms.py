from django import forms 
from django.db import models

from .models import AssignmentData, Assignment


class AssignmentDataForm(forms.ModelForm):
    class Meta:
        model = AssignmentData
        fields = [
            'assignment',
            'references',
            'location',
            'number1',
            'number2',
            'use_vehicle',
            'type',
            'use',
        ]
        
class AssignmentForm(forms.ModelForm):
    class Meta:
        model = Assignment
        fields = [
            'assignment',
            'references',
            'location',
            'number1',
            'number2',
            'use_vehicle',
            'type',
            'use',
        ]
