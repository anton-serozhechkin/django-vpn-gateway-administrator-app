from django.urls import path
from .views import *

urlpatterns = [
    path('', home, name='home'),
    path('change-user-<int:user_id>', change_user, name='change_user'),
    change_user
]
