from django.forms import ModelForm, forms
from django import forms
from .models import Users, Company


class UserForm(ModelForm):
    class Meta:
        model = Users
        fields = ['full_name', 'email', 'company']


class CompanyForm(ModelForm):
    class Meta:
        model = Company
        fields = ['name', 'size_limit']


class MonthForm(forms.Form):
    month = forms.DateField(widget=forms.DateInput(attrs={
                                                "placeholder": " Select a date",
                                                "class": "datepicker",
                                                "id": "datepicker",
                                                "name": "dateFilter"}))
