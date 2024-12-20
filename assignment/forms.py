from django import forms 
from django.db import models

from .models import OldAssignmentData, OldAssignment


class AssignmentDataForm(forms.ModelForm):
    class Meta:
        model = OldAssignmentData
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
        model = OldAssignment
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
