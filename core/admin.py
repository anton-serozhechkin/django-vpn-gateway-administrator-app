from django.contrib import admin
from .models import Company, Users, TransferLogs, Report

admin.site.register(Company)
admin.site.register(Users)
admin.site.register(TransferLogs)
admin.site.register(Report)