from django.shortcuts import render, reverse, redirect
from .models import Users, Report, Company
from .forms import UserChangeForm, CompanyChangeForm

def home(request):
    users = Users.objects.all()
    companies = Company.objects.all()
    reports = Report.objects.all()
    return render(request, 'home.html', locals())

def change_user(request, user_id):
    user = Users.objects.get(pk=user_id)
    if request.method == 'POST':
        form = UserChangeForm(request.POST, instance=user)
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
        form = UserChangeForm(instance=user)
    return render(request, 'change_user.html', locals())

def change_company(request, company_id):
    company = Company.objects.get(pk=company_id)
    if request.method == 'POST':
        form = CompanyChangeForm(request.POST, instance=company)
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
        form = CompanyChangeForm(instance=company)
    return render(request, 'change_company.html', locals())