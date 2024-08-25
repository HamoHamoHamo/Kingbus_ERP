from django import forms 
import re

from .models import Approval, Approver

class ApprovalForm(forms.ModelForm):
    class Meta:
        model = Approval
        fields = [
            'approval_type',
            'title',
            'content',
        ]

class ApproverForm(forms.ModelForm):
    class Meta:
        model = Approver
        fields = [
            'content',
            'status',
            'index',
        ]