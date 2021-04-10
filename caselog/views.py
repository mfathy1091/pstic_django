from django.shortcuts import render, redirect
from django.views import View
from .models import *
from django.db import connection
from .forms import *
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView
from datetime import datetime



class PSWorkersView(TemplateView):
    template_name = 'caselog/workers.html'

    def get(self, request, id=None, *args, **kwargs):
        psworkers = PsWorker.objects.all()
        context = {'psworkers': psworkers}
        return render(request, self.template_name, context)



class AddPsWorkerView(TemplateView):
    template_name = 'caselog/add_worker.html'
    psworkers = PsWorker.objects.all()
    genders = LogEntry.GENDER
    nationalities = LogEntry.NATIONALITY
    teams = PsWorker.TEAM

    def get(self, request):
        context = {
        'psworkers': self.psworkers,
        'genders': self.genders,
        'nationalities': self.nationalities,
        'teams':self.teams,
        }
        return render(request, self.template_name, context)
    
    def post(self, request):
        addpsworker_form = PSWorkerForm(request.POST)
        if addpsworker_form.is_valid():
            addpsworker_form.save()
            messages.success(request, ('Added Successfully'))
            return redirect ('caselog-dashboard')
        else:
            # Retrieved fields
            fullname = request.POST['fullname']
            age = request.POST['age']
            gender = request.POST['gender']
            nationality = request.POST['nationality']
            
            messages.success(request, ('There was an error'))
        
            contextAndRetriedvedFields = {
                'psworkers': self.psworkers,
                'genders': self.genders,
                'nationalities': self.nationalities,
                #'addpsworker_form': addpsworker_form,
                'fullname': fullname,
                'age': age,
                'gender': gender,
                'nationality': nationality,
                'teams':self.teams,
                }
            return render(request, self.template_name, contextAndRetriedvedFields)

class AddCaseView(TemplateView):
    template_name = 'caselog/add_case.html'
    cases = Case.objects.all()
    casetypes = LogEntry.CASETYPE
    months = LogEntry.MONTH
    genders = LogEntry.GENDER
    nationalities = LogEntry.NATIONALITY
    psworkers = PsWorker.objects.all()

    def get(self, request):
        context = {
        'case': self.cases,
        'casetypes': self.casetypes,
        'months': self.months,
        'genders': self.genders,
        'nationalities': self.nationalities,
        'psworkers': self.psworkers,
        }
        return render(request, self.template_name, context)

    def post(self, request):
        context = {
        'case': self.cases,
        'casetypes': self.casetypes,
        'months': self.months,
        'genders': self.genders,
        'nationalities': self.nationalities,
        'psworkers': self.psworkers,
        }
        form = AddCaseForm(request.POST)
        print('FORM STATUS')
        print(form.is_valid())
        if form.is_valid():
            # get fk objects selected from dropdowns fields
            casetype_obj = CaseType.objects.filter(id__exact=form.cleaned_data['casetype']).get()
            gender_obj = Gender.objects.filter(id__exact=form.cleaned_data['gender']).get()
            nationality_obj = Nationality.objects.filter(id__exact=form.cleaned_data['nationality']).get()
            month_obj = LogEntry.objects.filter(id__exact=form.cleaned_data['month']).get()

            # get values from input fields
            fullname = form.cleaned_data.get('fullname')
            filenum = form.cleaned_data['filenum']
            age = form.cleaned_data['age']

            # 1) create, fill, and save DirectBenef Object, then Case object
            dbenef_obj = DirectBenef(fullname=fullname, age=age, gender=gender_obj, nationality=nationality_obj)
            dbenef_obj.save()
            case_obj = Case(filenum=filenum, directbenef=dbenef_obj, casetype=casetype_obj)
            case_obj.save()

            messages.success(request, ('Added Successfully'))
            return render(request, self.template_name, context)
            #return redirect ('caselog-cases')
        else:
            print(form.errors)
            filenum = request.POST['filenum']
            fullname = request.POST['fullname']
            age = request.POST['age']
            #gender = request.POST['gender']
            #nationality = request.POST['nationality']
            #addpsworker_form = PSWorkerForm(request.POST) # refills the form if you instatioated the form naem in html form tag and removed the hard coded form
            
            messages.success(request, ('There was an error'))

            contextAndRetriedvedFields = {
            'case': self.cases,
            'casetypes': self.casetypes,
            'months': self.months,
            'genders': self.genders,
            'nationalities': self.nationalities,
            'psworkers': self.psworkers,
            
            'filenum': filenum,
            'fullname': fullname,
            'age': age,
            }
        return render(request, self.template_name, contextAndRetriedvedFields)


class CaseDetail(TemplateView):
    template_name = 'caselog/case_detail.html'

    def get(self, request, pk, *args, **kwargs):
        selectedlogentry_obj = LogEntry.objects.filter(id__exact=pk).get()
        selectedIndirectBenefs_qs = IndirectBenef.objects.filter(case_id__exact=selectedlogentry_obj.case)
        count = selectedIndirectBenefs_qs.count()

        print(selectedlogentry_obj)
        

        context = {
                    'selectedlogentry': selectedlogentry_obj,
                    'selectedIndirectBenefs': selectedIndirectBenefs_qs,
                    'count': count,
                    }
        return render(request, self.template_name, context)



    
class CaseView(TemplateView):


    template_name = 'caselog/cases.html'
    cases = Case.objects.all().select_related('directbenef')
    months = LogEntry.MONTH

    def get(self, request, id=None, *args, **kwargs):
        #  define a form to render it
        month_form = MonthForm()
        
        for case in self.cases:
            print(case.id, case.filenum)

        context = {
                    'cases': self.cases,
                    'month_form': month_form,
                    'months': self.months,
                    }
        return render(request, self.template_name, context)

    def post(self, request, id=None, *args, **kwargs):
        month_form = MonthForm(request.POST)
        if month_form.is_valid():
            selectedmonth = month_form.cleaned_data['month']
            #month_form = MonthForm() # to balnk the form

        context = {
                    'cases': self.cases,
                    'month_form': month_form,
                    'selectedmonth': selectedmonth,
                    'months': self.months,
                    }
        return render(request, self.template_name, context)


        
    
class LogEntriesView(TemplateView):
    query_statistics_cases_body = "SELECT \
        logentry.id, \
        logentry.nationality,\
        COUNT(logentry.id) AS total, \
        sum(case when logentry.age > 0 AND logentry.age <= 5 AND logentry.gender = \'Male\' Then 1 else 0 end) As age_0_5_M, \
        sum(case when logentry.age > 0 AND logentry.age <= 5 AND logentry.gender = \'Female\' Then 1 else 0 end) As age_0_5_F, \
        sum(case when logentry.age >= 6 AND logentry.age <= 9 AND logentry.gender = \'Male\' Then 1 else 0 end) As age_6_9_M, \
        sum(case when logentry.age >= 6 AND logentry.age <= 9 AND logentry.gender = \'Female\' Then 1 else 0 end) As age_6_9_F, \
        sum(case when logentry.age >= 10 AND logentry.age <= 14 AND logentry.gender = \'Male\' Then 1 else 0 end) As age_10_14_M, \
        sum(case when logentry.age >= 10 AND logentry.age <= 14 AND logentry.gender = \'Female\' Then 1 else 0 end) As age_10_14_F, \
        sum(case when logentry.age >= 15 AND logentry.age <= 17 AND logentry.gender = \'Male\' Then 1 else 0 end) As age_15_17_M, \
        sum(case when logentry.age >= 15 AND logentry.age <= 17 AND logentry.gender = \'Female\' Then 1 else 0 end) As age_15_17_F, \
        sum(case when logentry.age >= 18 AND logentry.age <= 24 AND logentry.gender = \'Male\' Then 1 else 0 end) As age_18_24_M, \
        sum(case when logentry.age >= 18 AND logentry.age <= 24 AND logentry.gender = \'Female\' Then 1 else 0 end) As age_18_24_F, \
        sum(case when logentry.age >= 25 AND logentry.age <= 49 AND logentry.gender = \'Male\' Then 1 else 0 end) As age_25_49_M, \
        sum(case when logentry.age >= 25 AND logentry.age <= 49 AND logentry.gender = \'Female\' Then 1 else 0 end) As age_25_49_F, \
        sum(case when logentry.age >= 50 AND logentry.age <= 59 AND logentry.gender = \'Male\' Then 1 else 0 end) As age_50_59_M, \
        sum(case when logentry.age >= 50 AND logentry.age <= 59 AND logentry.gender = \'Female\' Then 1 else 0 end) As age_50_59_F, \
        sum(case when logentry.age >= 60 AND logentry.gender = \'Male\' Then 1 else 0 end) As age_gt60_M, \
        sum(case when logentry.age >= 60 AND logentry.gender = \'Female\' Then 1 else 0 end) As age_gt60_F \
    FROM caselog_logentry AS logentry"


    query_statistics_cases_totals_row = "UNION \
        SELECT \
            logentry.id, \
            \"TOTAL\", \
            COUNT(logentry.id) AS total, \
            sum(case when logentry.age > 0 AND logentry.age <= 5 AND logentry.gender = \'Male\' Then 1 else 0 end) As age_0_5_M, \
            sum(case when logentry.age > 0 AND logentry.age <= 5 AND logentry.gender = \'Female\' Then 1 else 0 end) As age_0_5_F, \
            sum(case when logentry.age >= 6 AND logentry.age <= 9 AND logentry.gender = \'Male\' Then 1 else 0 end) As age_6_9_M, \
            sum(case when logentry.age >= 6 AND logentry.age <= 9 AND logentry.gender = \'Female\' Then 1 else 0 end) As age_6_9_F, \
            sum(case when logentry.age >= 10 AND logentry.age <= 14 AND logentry.gender = \'Male\' Then 1 else 0 end) As age_10_14_M, \
            sum(case when logentry.age >= 10 AND logentry.age <= 14 AND logentry.gender = \'Female\' Then 1 else 0 end) As age_10_14_F, \
            sum(case when logentry.age >= 15 AND logentry.age <= 17 AND logentry.gender = \'Male\' Then 1 else 0 end) As age_15_17_M, \
            sum(case when logentry.age >= 15 AND logentry.age <= 17 AND logentry.gender = \'Female\' Then 1 else 0 end) As age_15_17_F, \
            sum(case when logentry.age >= 18 AND logentry.age <= 24 AND logentry.gender = \'Male\' Then 1 else 0 end) As age_18_24_M, \
            sum(case when logentry.age >= 18 AND logentry.age <= 24 AND logentry.gender = \'Female\' Then 1 else 0 end) As age_18_24_F, \
            sum(case when logentry.age >= 25 AND logentry.age <= 49 AND logentry.gender = \'Male\' Then 1 else 0 end) As age_25_49_M, \
            sum(case when logentry.age >= 25 AND logentry.age <= 49 AND logentry.gender = \'Female\' Then 1 else 0 end) As age_25_49_F, \
            sum(case when logentry.age >= 50 AND logentry.age <= 59 AND logentry.gender = \'Male\' Then 1 else 0 end) As age_50_59_M, \
            sum(case when logentry.age >= 50 AND logentry.age <= 59 AND logentry.gender = \'Female\' Then 1 else 0 end) As age_50_59_F, \
            sum(case when logentry.age >= 60 AND logentry.gender = \'Male\' Then 1 else 0 end) As age_gt60_M, \
            sum(case when logentry.age >= 60 AND logentry.gender = \'Female\' Then 1 else 0 end) As age_gt60_F \
        FROM caselog_logentry AS logentry"




    template_name = 'caselog/logentries.html'
    logentries = LogEntry.objects.prefetch_related('case')
    cases = Case.objects.all().prefetch_related()
    months = LogEntry.MONTH
    nationalities = LogEntry.NATIONALITY
    

    def getstats(self):
        nationalities = LogEntry.NATIONALITY
        for nation in nationalities:
            logentries_per_nation = self.logentries.filter(dnationality__exact=nation)
            total_per_nation = logentries_per_nation.count()
            total_ages_0_5 = logentries_per_nation.filter(age__gte=0).filter(age__lte=5).count()
            total_ages_6_9 = logentries_per_nation.filter(age__gte=6).filter(age__lte=9).count()
            total_ages_10_14 = logentries_per_nation.filter(age__gte=10).filter(age__lte=14).count()
            total_ages_15_17 = logentries_per_nation.filter(age__gte=15).filter(age__lte=17).count()
            total_ages_18_24 = logentries_per_nation.filter(age__gte=18).filter(age__lte=24).count()
            total_ages_25_49 = logentries_per_nation.filter(age__gte=25).filter(age__lte=49).count()
            total_ages_50_59 = logentries_per_nation.filter(age__gte=50).filter(age__lte=59).count()
            total_ages_gt_60 = logentries_per_nation.filter(age__gte=60).count()

            
            print(logentries_per_nation)
            #print(nation, 
            #total_per_nation, 
            #total_ages_0_5, 
            #total_ages_6_9, 
            #total_ages_10_14, 
          #  total_ages_15_17, 
           # total_ages_18_24, 
           # total_ages_25_49,
           # total_ages_50_59,
           # total_ages_gt_60)



    def get(self, request, id=None, *args, **kwargs):
        logentries = LogEntry.objects.filter(month__exact="January").prefetch_related('case')

        query_statistics_new_cases = self.query_statistics_cases_body + " WHERE \
            logentry.month = 'January' AND logentry.casestatus = 'New' \
            GROUP BY nationality " + self.query_statistics_cases_totals_row + " WHERE \
            logentry.month = 'January' AND logentry.casestatus = 'New'"

        query_statistics_active_cases = self.query_statistics_cases_body + " WHERE \
            logentry.month = 'January' AND (logentry.casestatus = 'New' OR logentry.casestatus = 'Active') \
            GROUP BY nationality " + self.query_statistics_cases_totals_row + " WHERE \
            logentry.month = 'January' AND (logentry.casestatus = 'New' OR logentry.casestatus = 'Active')"

        rs_newstats = LogEntry.objects.raw(query_statistics_new_cases)
        rs_activestats = LogEntry.objects.raw(query_statistics_active_cases)

        month_form = MonthForm()

        context = {
                    'logentries': logentries,
                    'month_form': month_form,
                    'months': self.months,
                    'nationalities': self.nationalities,
                    'newstats': rs_newstats,
                    'activestats': rs_activestats,
                    'selectedmonth': 'January',
                    }
        return render(request, self.template_name, context)


    def post(self, request, id=None, *args, **kwargs):
        month_form = FilterByMonthForm(request.POST)
        if month_form.is_valid():
            selectedmonth = month_form.cleaned_data['month']
            selectedmonth_withqoutes = "'" + month_form.cleaned_data['month'] + "'"
            logentries = LogEntry.objects.filter(month__exact=selectedmonth).prefetch_related('case')

            query_statistics_new_cases = self.query_statistics_cases_body + " WHERE \
                logentry.month = " + selectedmonth_withqoutes + " AND logentry.casestatus = 'NEW' \
                GROUP BY nationality " + self.query_statistics_cases_totals_row + " WHERE \
                logentry.month = " + selectedmonth_withqoutes + " AND logentry.casestatus = 'NEW'"

            query_statistics_active_cases = self.query_statistics_cases_body + " WHERE \
                logentry.month = " + selectedmonth_withqoutes + " AND (logentry.casestatus = 'NEW' OR logentry.casestatus = 'Ongoing') \
                GROUP BY nationality " + self.query_statistics_cases_totals_row + " WHERE \
                logentry.month = " + selectedmonth_withqoutes + " AND (logentry.casestatus = 'NEW' OR logentry.casestatus = 'Ongoing')"

            rs_newstats = LogEntry.objects.raw(query_statistics_new_cases)
            rs_activestats = LogEntry.objects.raw(query_statistics_active_cases)
            
            context = {
                    'cases': self.cases,
                    'logentries': logentries,
                    'month_form': month_form,
                    'months': self.months,
                    'newstats': rs_newstats,
                    'activestats': rs_activestats,
                    'selectedmonth': selectedmonth,
                    }
            return render(request, self.template_name, context)
        else:
            messages.success(request, ('There was an error'))
        
            contextAndRetriedvedFields = {
                    'cases': self.cases,
                    'month_form': month_form,
                    'months': self.months,
                    }
            return render(request, self.template_name, contextAndRetriedvedFields)

    

class AddLogEntry(TemplateView):
    template_name = 'caselog/add_logentry.html'
    cases = Case.objects.all()
    casetypes = LogEntry.CASETYPE
    casestatuses = LogEntry.CASESTATUS
    months = LogEntry.MONTH
    genders = LogEntry.GENDER
    nationalities = LogEntry.NATIONALITY
    locations = LogEntry.LOCATION
    referralsources = LogEntry.REFERRALSOURCE
    psworkers = PsWorker.objects.all()

    def get(self, request):
        context = {
        'case': self.cases,
        'casetypes': self.casetypes,
        'casestatuses': self.casestatuses,
        'months': self.months,
        'genders': self.genders,
        'nationalities': self.nationalities,
        'locations': self.locations,
        'referralsources': self.referralsources,
        'psworkers': self.psworkers,
        }
        return render(request, self.template_name, context)

    def post(self, request):
        context = {
        'case': self.cases,
        'casetypes': self.casetypes,
        'casestatuses': self.casestatuses,
        'months': self.months,
        'genders': self.genders,
        'nationalities': self.nationalities,
        'psworkers': self.psworkers,
        }
        form = AddLogEntryForm(request.POST)
        print('FORM STATUS')
        print(form.is_valid())
        if form.is_valid():
            # get fk objects selected from dropdowns fields
            #month_obj = Month.objects.filter(id__exact=form.cleaned_data['month']).get()

            # get values from input fields
            month = form.cleaned_data.get('month')
            casestatus = form.cleaned_data.get('casestatus')
            casetype = form.cleaned_data.get('casetype')
            filenum = form.cleaned_data['filenum']
            age = form.cleaned_data['age']
            fullname = form.cleaned_data.get('fullname')
            gender = form.cleaned_data.get('gender')
            nationlaity = form.cleaned_data.get('nationality')
            phone = form.cleaned_data.get('phone')
            location = form.cleaned_data.get('location')
            referralsource = form.cleaned_data.get('referralsource')
            psworkerid = form.cleaned_data.get('psworker')


            # get pk of foreing tables
            psworker_obj = PsWorker.objects.filter(id__exact=psworkerid).get()

            # 1) create, fill, and save CaseObject then LogEntry Object            
            case_obj = Case(filenum= filenum)
            case_obj.save()
            


            logentry_obj = LogEntry(case=case_obj, casestatus= casestatus, month= month, casetype=casetype, age= age, fullname= fullname, gender=gender, nationality=nationlaity, phone=phone, location=location, referralsource=referralsource, psworker=psworker_obj)
            logentry_obj.save()

            messages.success(request, ('Added Successfully'))
            return render(request, self.template_name, context)
            #return redirect ('caselog-cases')
        else:
            print(form.errors)
            filenum = request.POST['filenum']
            fullname = request.POST['fullname']
            age = request.POST['age']
            phone = request.POST['phone']
            #gender = request.POST['gender']
            #nationality = request.POST['nationality']
            #addpsworker_form = PSWorkerForm(request.POST) # refills the form if you instatioated the form naem in html form tag and removed the hard coded form
            
            messages.success(request, ('There was an error'))

            contextAndRetriedvedFields = {
            'case': self.cases,
            'casestatuses': self.casestatuses,
            'casetypes': self.casetypes,
            'months': self.months,
            'genders': self.genders,
            'nationalities': self.nationalities,
            'locations': self.locations,
            'referralsources': self.referralsources,
            'psworkers': self.psworkers,
            
            'filenum': filenum,
            'fullname': fullname,
            'age': age,
            }
        return render(request, self.template_name, contextAndRetriedvedFields)
            


def beneficiaries(request):
    rs_beneficiaries = getResultSet(query_beneficiaries)
    rs_statistics_new_all_benificiaries = getResultSet(query_statistics_new_all_benificiaries)
    rs_statistics_active_all_benificiaries = getResultSet(query_statistics_active_all_benificiaries)

    context = {
            'beneficiaries': rs_beneficiaries,
            'statistics_new_all_benificiaries': rs_statistics_new_all_benificiaries,
            'statistics_active_all_benificiaries': rs_statistics_active_all_benificiaries,
            }

    return render(request, 'caselog/beneficiaries.html', context)



class Queries():
    allpsworkers = PsWorker.objects.all()

    alllogentries = LogEntry.objects.prefetch_related('case', 'psworker')
    nc_entries = alllogentries.filter(psworker__team='NC')
    cairo_entries = alllogentries.filter(psworker__team='Cairo')
    
    ncpsworkers = PsWorker.objects.filter(team__exact="NC")
    cairopsworkers = PsWorker.objects.filter(team__exact="Cairo")

    
    #cairoentries = LogEntry.objects.prefetch_related('case', 'psworker').filter(psworker.team__exact="Cairo")





class Dashboard(TemplateView):
    template_name = 'caselog/dashboard.html'


    def getWorkersStats(self, query):
        workers_stats_list =[]
        workers_query = query

        for worker in workers_query:
            entries = worker.logentry_set.prefetch_related('logentries')
            jan_entries_count = entries.filter(month__exact = 'January').count()
            feb_entries_count = entries.filter(month__exact = 'February').count()
            mar_entries_count = entries.filter(month__exact = 'March').count()
            apr_entries_count = entries.filter(month__exact = 'April').count()
            
            workers_stats_list.append([worker.id, worker.fullname, jan_entries_count, feb_entries_count, mar_entries_count, apr_entries_count])

        return workers_stats_list
    
    def getTotalStats(self, query):

        total_stats_list = []
        totalentries_query = query

        jan_entries_count = totalentries_query.filter(month__exact = 'January').count()
        feb_entries_count = totalentries_query.filter(month__exact = 'February').count()
        mar_entries_count = totalentries_query.filter(month__exact = 'March').count()
        apr_entries_count = totalentries_query.filter(month__exact = 'April').count()

        total_stats_list.append(["", "", jan_entries_count, feb_entries_count, mar_entries_count, apr_entries_count])

        return total_stats_list


    def get(self, request):
        
        entries_month = LogEntry.objects.prefetch_related('case', 'psworker').filter(month__exact='April')
        total_cases_month = entries_month.count()
        #new = entries_month.filter(casestatus='New').count()
        #ongoing = entries_month.filter(casestatus='Ongoing').count()
        
        # Alex
        stats_nc_workers = self.getWorkersStats(Queries.ncpsworkers)
        stats_nc_entriestotal = self.getTotalStats(Queries.nc_entries)
        
        # Cairo
        stats_cairo_workers = self.getWorkersStats(Queries.cairopsworkers)
        stats_cairo_entriestotal = self.getTotalStats(Queries.cairo_entries)

        context = {
            'allpsworkers': Queries.allpsworkers,
            'total_cases_month': total_cases_month,
            #'new': new,
            #'ongoing': ongoing,
            'allentries': Queries.alllogentries,
            'stats_nc_workers':stats_nc_workers,
            'stats_nc_entriestotal':stats_nc_entriestotal,
            'stats_cairo_entriestotal': stats_cairo_entriestotal,
            'stats_cairo_workers':stats_cairo_workers,
        }

        return render(request, self.template_name, context)

class PsWorkerView(TemplateView):
    template_name = 'caselog/psworker.html'
    #logentries = LogEntry.objects.prefetch_related('case')
    cases = Case.objects.all().prefetch_related()
    months = LogEntry.MONTH
    nationalities = LogEntry.NATIONALITY

    def get(self, request, pk_test):
        psworker = PsWorker.objects.get(id=pk_test)
        psworker_logentries = psworker.logentry_set.all()
        psworker_logentries_count = psworker_logentries.count()

        context={
            'psworker': psworker,
            'psworker_logentries': psworker_logentries,
            'psworker_logentries_count': psworker_logentries_count,
            'months': self.months,
            'selectedmonth': 'All',
        }

        return render(request, self.template_name, context)


        
class UpdateLogEntry(TemplateView):
    template_name = 'caselog/add_logentry.html'
    cases = Case.objects.all()
    casetypes = LogEntry.CASETYPE
    casestatuses = LogEntry.CASESTATUS
    months = LogEntry.MONTH
    genders = LogEntry.GENDER
    nationalities = LogEntry.NATIONALITY
    locations = LogEntry.LOCATION
    referralsources = LogEntry.REFERRALSOURCE
    psworkers = PsWorker.objects.all()

    def get(self, request, pk):
        context = {
        'case': self.cases,
        'casetypes': self.casetypes,
        'casestatuses': self.casestatuses,
        'months': self.months,
        'genders': self.genders,
        'nationalities': self.nationalities,
        'locations': self.locations,
        'referralsources': self.referralsources,
        'psworkers': self.psworkers,
        }
        return render(request, self.template_name, context)

    def post(self, request):
        context = {
        'case': self.cases,
        'casetypes': self.casetypes,
        'casestatuses': self.casestatuses,
        'months': self.months,
        'genders': self.genders,
        'nationalities': self.nationalities,
        'psworkers': self.psworkers,
        }
        form = AddLogEntryForm(request.POST)
        print('FORM STATUS')
        print(form.is_valid())
        if form.is_valid():
            # get fk objects selected from dropdowns fields
            #month_obj = Month.objects.filter(id__exact=form.cleaned_data['month']).get()

            # get values from input fields
            month = form.cleaned_data.get('month')
            casestatus = form.cleaned_data.get('casestatus')
            casetype = form.cleaned_data.get('casetype')
            filenum = form.cleaned_data['filenum']
            age = form.cleaned_data['age']
            fullname = form.cleaned_data.get('fullname')
            gender = form.cleaned_data.get('gender')
            nationlaity = form.cleaned_data.get('nationality')
            phone = form.cleaned_data.get('phone')
            location = form.cleaned_data.get('location')
            referralsource = form.cleaned_data.get('referralsource')

            # 1) create, fill, and save CaseObject then LogEntry Object            
            case_obj = Case(filenum= filenum)
            case_obj.save()
            
            logentry_obj = LogEntry(case=case_obj, casestatus= casestatus, month= month, casetype=casetype, age= age, fullname= fullname, gender=gender, nationality=nationlaity, phone=phone, location=location, referralsource=referralsource)
            logentry_obj.save()

            messages.success(request, ('Added Successfully'))
            return render(request, self.template_name, context)
            #return redirect ('caselog-cases')
        else:
            print(form.errors)
            filenum = request.POST['filenum']
            fullname = request.POST['fullname']
            age = request.POST['age']
            phone = request.POST['phone']
            #gender = request.POST['gender']
            #nationality = request.POST['nationality']
            #addpsworker_form = PSWorkerForm(request.POST) # refills the form if you instatioated the form naem in html form tag and removed the hard coded form
            
            messages.success(request, ('There was an error'))

            contextAndRetriedvedFields = {
            'case': self.cases,
            'casetypes': self.casetypes,
            'months': self.months,
            'genders': self.genders,
            'nationalities': self.nationalities,
            'locations': self.locations,
            'referralsources': self.referralsources,
            'psworkers': self.psworkers,
            
            'filenum': filenum,
            'fullname': fullname,
            'age': age,
            }
        return render(request, self.template_name, contextAndRetriedvedFields)
            

