from django.shortcuts import render, reverse, redirect
from .models import Users, Report, Company, TransferLogs
from .forms import UserForm, CompanyForm, MonthForm
from .sub_modules import getter_company, getter_user
from faker import Faker
import random
from datetime import datetime, timedelta
from decimal import Decimal


fake = Faker()

def from_bytes_to_tb(size_traffic):
    terabite = 1099511627776 / int(size_traffic)
    return Decimal(round(terabite, 2))


def home(request):
    users = Users.objects.all()
    companies = Company.objects.all()
    reports = Report.objects.all()
    if request.method == 'POST':
        month_form = MonthForm(request.POST)
        if 'generate_data' in request.POST:
            for _ in range(2):
                random_company = Company.objects.order_by('?')[0]
                new_user = Users.objects.create(full_name=fake.name(),
                                                email=fake.email(),
                                                company=random_company)
                for __ in range(random.randint(50, 200)):
                    random_date = fake.date_between(start_date='-150d', end_date='today')
                    random_url = fake.url()
                    random_size_traffic = fake.random_int(min=100, max=10995116277760)
                    TransferLogs.objects.create(user=new_user, date=random_date,
                                                recource=random_url, transferred=random_size_traffic)
                    report_exist = Report.objects.filter(date_start__month=random_date.month, company=new_user.company)
                    traffic_used = from_bytes_to_tb(random_size_traffic)
                    if report_exist:
                        update_report = Report.objects.get(date_start__month=random_date.month,
                                                           company=new_user.company)
                        update_report.traffic_used += traffic_used
                        update_report.save()
                    else:
                        data_end = random_date+timedelta(days=30)
                        new_report = Report.objects.create(date_start=random_date,
                                                           date_end=data_end,
                                                           company=new_user.company,
                                                           traffic_used=traffic_used)
            for report in reports:
                company_limit = Company.objects.get(name=report.company.name).size_limit
                if report.traffic_used > company_limit:
                    report.more_than_limit = True
                    report.exceeding_limit = report.traffic_used - company_limit
                    report.save()
            return redirect('home')

        elif 'show_for_period' in  request.POST:
            if month_form.is_valid():
                month = month_form.cleaned_data.get('month').month
                reports = Report.objects.filter(date_start__month=month, more_than_limit=True).order_by('-traffic_used')
                if not reports.exists():
                    no_violations = 'No violations were found this month'
        else:
            pass
    else:
        month_form = MonthForm()
    return render(request, 'home.html', locals())


def add_user(request):
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
        else:
            return redirect('add_user')
    else:
        form = UserForm()
    return render(request, 'add/add_user.html', locals())


def change_user(request, user_id):
    user = getter_user(user_id)
    if request.method == 'POST':
        form = UserForm(request.POST, instance=user)
        if form.is_valid():
            if not form.has_changed():
                return redirect('home')
            else:
                instance = form.save(commit=False)
                instance.full_name = form.cleaned_data['full_name']
                instance.email = form.cleaned_data['email']
                instance.company = form.cleaned_data['company']
                instance.save()
                return redirect('home')
        else:
            return redirect(reverse('change_user', kwargs={'user_id': user_id}))
    else:
        form = UserForm(instance=user)
    return render(request, 'change/change_user.html', locals())


def add_company(request):
    if request.method == 'POST':
        form = CompanyForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
        else:
            return redirect('add_company')
    else:
        form = CompanyForm()
    return render(request, 'add/add_company.html', locals())


def change_company(request, company_id):
    company = getter_company(company_id)
    if request.method == 'POST':
        form = CompanyForm(request.POST, instance=company)
        if form.is_valid():
            if not form.has_changed():
                return redirect('home')
            else:
                instance = form.save(commit=False)
                instance.name = form.cleaned_data['name']
                instance.size_limit = form.cleaned_data['size_limit']
                instance.save()
                return redirect('home')
        else:
            return redirect(reverse('change_company', kwargs={'company_id': company_id}))
    else:
        form = CompanyForm(instance=company)
    return render(request, 'change/change_company.html', locals())

def delete_user(request, user_id):
    getter_user(user_id).delete()
    return redirect('home')

def delete_company(request, company_id):
    getter_company(company_id).delete()
    return redirect('home')

def delete_all_user(request):
    Users.objects.all().delete()
    return redirect('home')