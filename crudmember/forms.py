from django import forms
from .models import User, Client

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

class ClientForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = [
            'business_num',
            'name',
            'representative',
            'phone',
            'manager',
            'manager_phone',
            'email',
            'address',
            'note',
        ]