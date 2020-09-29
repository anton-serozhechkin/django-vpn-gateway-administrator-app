from django.shortcuts import render, reverse, redirect
from .models import Users, Report, Company
from .forms import UserForm, CompanyForm

def home(request):
    users = Users.objects.all()
    companies = Company.objects.all()
    reports = Report.objects.all()
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
    return render(request, 'add_user.html', locals())

def change_user(request, user_id):
    user = Users.objects.get(pk=user_id)
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
    return render(request, 'change_user.html', locals())

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
    return render(request, 'add_company.html', locals())

def change_company(request, company_id):
    company = Company.objects.get(pk=company_id)
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
    return render(request, 'change_company.html', locals())