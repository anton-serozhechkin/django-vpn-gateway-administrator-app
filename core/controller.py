from .models import Users, Report, Company, TransferLogs
from .forms import UserForm, MonthForm
from .sub_modules import getter_company, getter_user
from faker import Faker
import random
from datetime import datetime, timedelta
from decimal import Decimal


class IndexController:
    
    
    def __init__(self, request):
        self._request = request
        self.__fake = Faker()
        self._users = Users.objects.all()
        self._companies = Company.objects.all()
        self._reports = Report.objects.all()

    
    def __from_bytes_to_tb(self, random_size_traffic):
        terabite = 1099511627776 / int(random_size_traffic)
        return Decimal(round(terabite, 2))
    

    def __add_flags_exceeding_limit(self):
        for report in self._reports:
            company_limit = Company.objects.get(name=report.company.name).size_limit
            if report.traffic_used > company_limit:
                report.more_than_limit = True
                report.exceeding_limit = report.traffic_used - company_limit
                report.save()


    def __generate_data(self):
        for _ in range(5):
            random_company = Company.objects.order_by('?')[0]
            new_user = Users.objects.create(full_name=self.__fake.name(),
                                            email=self.__fake.email(),
                                            company=random_company)
            for __ in range(random.randint(50, 200)):
                random_date = self.__fake.date_between(start_date='-150d', end_date='today')
                random_data_end = random_date + timedelta(days=30)
                random_size_traffic = self.__fake.random_int(min=100, max=10995116277760)
                TransferLogs.objects.create(user=new_user, date=random_date,
                                            recource=self.__fake.url(), transferred=random_size_traffic)
                report_exist = Report.objects.filter(date_start__month=random_date.month,
                                                     company=new_user.company).exists()
                count_traffic_used = self.__from_bytes_to_tb(random_size_traffic)
                if report_exist:
                    update_report = Report.objects.get(date_start__month=random_date.month,
                                                       company=new_user.company)
                    update_report.traffic_used += count_traffic_used
                    update_report.save()
                else:
                    new_report = Report.objects.create(date_start=random_date,
                                                       date_end=random_data_end,
                                                       company=new_user.company,
                                                       traffic_used=count_traffic_used)
        self.__add_flags_exceeding_limit()


    def _prepare_responce_post(self):
        month_form = MonthForm(self._request.POST)
        if 'generate_data' in self._request.POST:
            self.__generate_data()
            return self._users, self._companies, self._reports, month_form
        elif 'show_for_period' in  self._request.POST:
            month = month_form.cleaned_data.get('month').month
            reports = Report.objects.filter(date_start__month=month, more_than_limit=True).order_by('-traffic_used')
            if not reports.exists():
                reports = 'No violations were found this month'
            return self._users, self._companies, reports, month_form

    
    def _prepare_responce_get(self):
        month_form = MonthForm()
        return self._users, self._companies, self._reports, month_form
        

    #def _responce(self):
    #    if self.__request.method == 'POST':
    #        responce = self.__prepare_responce_post()
    #    else:
    #        responce = self.__prepare_responce_get()
