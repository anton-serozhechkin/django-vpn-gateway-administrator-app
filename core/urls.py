from django.urls import path
from .views import *

urlpatterns = [
    path('', home, name='home'),
    path('change-user/<int:user_id>', change_user, name='change_user'),
    path('change-company/<int:company_id>', change_company, name='change_company'),
    path('delete-user/<int:user_id>', delete_user, name='delete_user'),
    path('delete-company/<int:company_id>', delete_company, name='delete_company'),
    path('add-user', add_user, name='add_user'),
    path('add-company', add_company, name='add_company'),
]
