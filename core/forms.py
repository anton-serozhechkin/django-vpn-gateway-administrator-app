from django.forms import ModelForm
from .models import Users, Company

class UserChangeForm(ModelForm):
    class Meta:
        model = Users
        fields = ['full_name', 'email', 'company']

class CompanyChangeForm(ModelForm):
    class Meta:
        model = Company
        fields = ['name', 'size_limit']