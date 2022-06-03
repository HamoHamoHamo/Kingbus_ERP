from django import forms
from .models import User

class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = [
            'user_id',
            'company',
            'company_tel',
            'company_address',
            'registeration_num',
            'name',
            'manager_tel',
            'manager_mail',
        ]