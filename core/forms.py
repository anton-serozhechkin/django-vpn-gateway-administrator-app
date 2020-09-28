from django import forms
from .models import *

class UserChangeForm(forms.Form):
    full_name = forms.CharField()
    email = forms.EmailField(required=False)
    company = forms.ModelChoiceField(queryset=Company.objects.all())