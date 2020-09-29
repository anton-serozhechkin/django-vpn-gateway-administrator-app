from django.db import models
from datetime import datetime, timedelta
from django.shortcuts import reverse

class Company(models.Model):
    name = models.CharField('Company name', max_length=30)
    size_limit = models.IntegerField('Traffic limit for a month(in TB)')
    
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = 'Company'
        verbose_name_plural = 'Companies'

class Users(models.Model):
    full_name = models.CharField('Full name', max_length=40)
    email = models.EmailField('Email', null=True, blank=True)
    company = models.ForeignKey(Company, on_delete=models.CASCADE, verbose_name='Company')

    def __str__(self):
        return 'User {} || company {}'.format(self.full_name, self.company)
    
    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'

class TransferLogs(models.Model):
    user = models.ForeignKey(Users, on_delete=models.CASCADE, verbose_name='User')
    date = models.DateTimeField('Date n time of transfer', default=datetime.now())
    recource = models.CharField('Recourse', max_length=40)
    transferred = models.BigIntegerField('Was transferred(in bytes)')

    def __str__(self):
        return 'User {} transferred {} into {}'.format(self.user.full_name, self.transferred, self.recource)
    
    class Meta:
        verbose_name = 'Transfer log'
        verbose_name_plural = 'Transfer logs'

class Report(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE, verbose_name='Company')
    traffic_used = models.IntegerField('Was used (in TB)', default=0)
    date_start = models.DateField('Date start of using traffic', default=datetime.now())
    date_end = models.DateField('Date end of using traffic', default=datetime.now()+timedelta(days=30))

    def __str__(self):
        return self.company.name
    
    class Meta:
        verbose_name = 'Report'
        verbose_name_plural = 'Reports'

    
"""
    users - id, name, email, company(fk name) :edit remove add(by id company)+ validation(email, non empty) : add company by dropdown
companies - id, name, size : validation for adding
tranfer logs - user, datetime, resource, transferred
report - company, used, quota, difference, date
"""