from django.urls import path
from .views import home, change_user, change_company

urlpatterns = [
    path('', home, name='home'),
    path('change-user/<int:user_id>', change_user, name='change_user'),
    path('change-company/<int:company_id>', change_company, name='change_company'),
]
