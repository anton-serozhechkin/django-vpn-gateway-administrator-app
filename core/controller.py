from .models import Users, Report, Company, TransferLogs
from .forms import UserForm, MonthForm
from faker import Faker
import random
from decimal import Decimal


class IndexController:
    
    
    def __init__(self, request):
        self._request = request
        self.__fake = Faker()
        self._users = Users.objects.all()
        self._companies = Company.objects.all()
        self._reports = Report.objects.all()

    
    def __from_bytes_to_tb(self, random_size_traffic):
        # format bytes to terabyte
        terabite = Decimal(round(1099511627776 / int(random_size_traffic), 2))
        return terabite
    

    def __add_flags_exceeding_limit(self):
        # iterate ny all report objects
        for report in self._reports:
            company_limit = Company.objects.get(name=report.company.name).size_limit
            # check if traffic_used more than limit 
            if report.traffic_used > company_limit:
                # update report
                report.more_than_limit = True
                report.exceeding_limit = report.traffic_used - company_limit
                report.save()


    def __generate_data(self):
        for _ in range(15):
            # get random company
            random_company = Company.objects.order_by('?')[0]
            # create new user
            new_user = Users.objects.create(full_name=self.__fake.name(),
                                            email=self.__fake.email(),
                                            company=random_company)
            for __ in range(random.randint(50, 200)):
                # create random var random_date
                random_date = self.__fake.date_between(start_date='-150d', end_date='today')
                # create random var random_size_traffic 
                random_size_traffic = self.__fake.random_int(min=100, max=10995116277760)
                # create new transfer log
                TransferLogs.objects.create(user=new_user, date=random_date,
                                            recource=self.__fake.url(), transferred=random_size_traffic)
                # check if report exist
                report_exist = Report.objects.filter(date_start__month=random_date.month,
                                                     company=new_user.company).exists()
                # transfer bytes to tb
                count_traffic_used = self.__from_bytes_to_tb(random_size_traffic)
                if report_exist:
                    # update attr traffic_used for company
                    update_report = Report.objects.get(date_start__month=random_date.month,
                                                       company=new_user.company)
                    update_report.traffic_used += count_traffic_used
                    update_report.save()
                else:
                    # create new report
                    date_start = '2020-{}-01'.format(random_date.month)
                    date_end = '2020-{}-30'.format(random_date.month)
                    new_report = Report.objects.create(date_start=date_start,
                                                       date_end=date_end,
                                                       company=new_user.company,
                                                       traffic_used=count_traffic_used)
        # call func thar add flags if exceeding limit for company 
        self.__add_flags_exceeding_limit()


    def __prepare_responce_post(self):
        # get form from post request
        month_form = MonthForm(self._request.POST)
        if 'generate_data' in self._request.POST:
            # call func generate data  
            self.__generate_data()
            return self._users, self._companies, self._reports, month_form
        elif 'show_for_period' in  self._request.POST:
            if month_form.is_valid():
                # get month from form
                month = month_form.cleaned_data.get('month').month
                reports = Report.objects.filter(date_start__month=month, more_than_limit=True).order_by('-traffic_used')
                # if report for month isnt exist
                if not reports.exists():
                    reports = 'No violations were found this month'
                return self._users, self._companies, reports, month_form
        elif 'show_all_reports' in  self._request.POST:
            return self._users, self._companies, self._reports, month_form


    def __prepare_responce_get(self):
        month_form = MonthForm()
        return self._users, self._companies, self._reports, month_form


    def _responce(self):
        # get responce for view
        if self._request.method == 'POST':
            users, companies, reports, month_form = self.__prepare_responce_post()
        else:
            users, companies, reports, month_form = self.__prepare_responce_get()
        return users, companies, reports, month_form
