from django import forms
from notice.models import Notice

class NoticeForm(forms.ModelForm):
    class Meta:
        model = Notice
        fields = ['title', 'content', 'kinds']
        kinds_choices = [('office','Office'), ('driver', 'Driver')]
        widgets = {
            'kinds':forms.RadioSelect(
                choices=kinds_choices,
                attrs={'class': 'form-control'}
            )
        }