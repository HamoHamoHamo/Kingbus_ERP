from django import forms 
from django.db import models

from .models import DispatchOrder, DispatchConsumer, DispatchRoute, DispatchInfo

class OrderForm(forms.ModelForm):
    class Meta:
        model = DispatchOrder
        field =
    