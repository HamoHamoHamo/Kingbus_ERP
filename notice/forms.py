from django import forms
from models import Notice

class Notice(forms.ModelForm):
    class Meta:
        model = Notice
        fields = ['creator', 'title', 'content', 'kinds']