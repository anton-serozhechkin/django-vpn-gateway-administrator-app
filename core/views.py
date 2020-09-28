from django.shortcuts import render, reverse, redirect
from .models import *
from .forms import *

def home(request):
    users = Users.objects.all()
    companies = Company.objects.all()
    reports = Report.objects.all()
    return render(request, 'home.html', locals())

def change_user(request, user_id):
    user = User.objects.get(pk=user_id)
    if request.method == 'POST':
        form = UserChangeForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data()
            return redirect('home')
        else:
            return redirect(reverse('change_user', kwargs={'user_id': user_id}))
    else:
        form = UserChangeForm()
    return render(request, 'change_user.html')