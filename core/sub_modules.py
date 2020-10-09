from .models import Users, Company

def getter_user(user_id):
    user = Users.objects.get(pk=user_id)
    return user

def getter_company(company_id):
    company = Company.objects.get(pk=company_id)
    return company