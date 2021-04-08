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
        conselectedmonth = {'psworkers': psworkers}
        return render(request, self.template_name, conselectedmonth)



class AddPsWorkerView(TemplateView):
    template_name = 'caselog/add_worker.html'
    psworkers = PsWorker.objects.all()
    genders = LogEntry.GENDER
    nationalities = LogEntry.NATIONALITY

    def get(self, request):
        #  define a blank form to render it
        #addpsworker_form = PSWorkerForm()

        conselectedmonth = {
        'psworkers': self.psworkers,
        'genders': self.genders,
        'nationalities': self.nationalities,
        #'addpsworker_form':addpsworker_form,
        }
        return render(request, self.template_name, conselectedmonth)
    
    def post(self, request):
        addpsworker_form = PSWorkerForm(request.POST)
        if addpsworker_form.is_valid():
            addpsworker_form.save()
            messages.success(request, ('Added Successfully'))
            return redirect ('caselog-workers')
        else:
            # Retrieved fields
            fullname = request.POST['fullname']
            age = request.POST['age']
            gender = request.POST['gender']
            nationality = request.POST['nationality']
            #selectedmonth = addpsworker_form.cleaned_data['fullname']
            #addpsworker_form = PSWorkerForm(request.POST) # refills the form if you instatioated the form naem in html form tag and removed the hard coded form
            
            messages.success(request, ('There was an error'))
        
            conselectedmonthAndRetriedvedFields = {
                'psworkers': self.psworkers,
                'genders': self.genders,
                'nationalities': self.nationalities,
                #'addpsworker_form': addpsworker_form,
                'fullname': fullname,
                'age': age,
                'gender': gender,
                'nationality': nationality,
                }
            return render(request, self.template_name, conselectedmonthAndRetriedvedFields)

class AddCaseView(TemplateView):
    template_name = 'caselog/add_case.html'
    cases = Case.objects.all()
    casetypes = LogEntry.CASETYPE
    months = LogEntry.MONTH
    genders = LogEntry.GENDER
    nationalities = LogEntry.NATIONALITY
    psworkers = PsWorker.objects.all()

    def get(self, request):
        conselectedmonth = {
        'case': self.cases,
        'casetypes': self.casetypes,
        'months': self.months,
        'genders': self.genders,
        'nationalities': self.nationalities,
        'psworkers': self.psworkers,
        }
        return render(request, self.template_name, conselectedmonth)

    def post(self, request):
        conselectedmonth = {
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
            return render(request, self.template_name, conselectedmonth)
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

            conselectedmonthAndRetriedvedFields = {
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
        return render(request, self.template_name, conselectedmonthAndRetriedvedFields)



class AddLogEntry(TemplateView):
    template_name = 'caselog/add_worker.html'
    psworkers = PsWorker.objects.all()
    genders = LogEntry.GENDER
    nationalities = LogEntry.NATIONALITY

    def get(self, request):
        #  define a blank form to render it
        #addpsworker_form = PSWorkerForm()

        conselectedmonth = {
        'psworkers': self.psworkers,
        'genders': self.genders,
        'nationalities': self.nationalities,
        #'addpsworker_form':addpsworker_form,
        }
        return render(request, self.template_name, conselectedmonth)
    
    def post(self, request):
        addpsworker_form = PSWorkerForm(request.POST)
        if addpsworker_form.is_valid():
            addpsworker_form.save()
            messages.success(request, ('Added Successfully'))
            return redirect ('caselog-workers')
        else:
            # Retrieved fields
            fullname = request.POST['fullname']
            age = request.POST['age']
            gender = request.POST['gender']
            nationality = request.POST['nationality']
            #selectedmonth = addpsworker_form.cleaned_data['fullname']
            #addpsworker_form = PSWorkerForm(request.POST) # refills the form if you instatioated the form naem in html form tag and removed the hard coded form
            
            messages.success(request, ('There was an error'))
        
            conselectedmonthAndRetriedvedFields = {
                'psworkers': self.psworkers,
                'genders': self.genders,
                'nationalities': self.nationalities,
                #'addpsworker_form': addpsworker_form,
                'fullname': fullname,
                'age': age,
                'gender': gender,
                'nationality': nationality,
                }
            return render(request, self.template_name, conselectedmonthAndRetriedvedFields)



class CaseDetail(TemplateView):
    template_name = 'caselog/case_detail.html'

    def get(self, request, pk, *args, **kwargs):
        selectedlogentry_obj = LogEntry.objects.filter(id__exact=pk).get()
        selectedIndirectBenefs_qs = IndirectBenef.objects.filter(case_id__exact=selectedlogentry_obj.case)
        count = selectedIndirectBenefs_qs.count()

        print(selectedlogentry_obj)
        

        conselectedmonth = {
                    'selectedlogentry': selectedlogentry_obj,
                    'selectedIndirectBenefs': selectedIndirectBenefs_qs,
                    'count': count,
                    }
        return render(request, self.template_name, conselectedmonth)



    
class CaseView(TemplateView):


    template_name = 'caselog/cases.html'
    cases = Case.objects.all().select_related('directbenef')
    months = LogEntry.MONTH

    def get(self, request, id=None, *args, **kwargs):
        #  define a form to render it
        month_form = MonthForm()
        
        for case in self.cases:
            print(case.id, case.filenum)

        conselectedmonth = {
                    'cases': self.cases,
                    'month_form': month_form,
                    'months': self.months,
                    }
        return render(request, self.template_name, conselectedmonth)

    def post(self, request, id=None, *args, **kwargs):
        month_form = MonthForm(request.POST)
        if month_form.is_valid():
            selectedmonth = month_form.cleaned_data['month']
            #month_form = MonthForm() # to balnk the form

        conselectedmonth = {
                    'cases': self.cases,
                    'month_form': month_form,
                    'selectedmonth': selectedmonth,
                    'months': self.months,
                    }
        return render(request, self.template_name, conselectedmonth)


        
    
class LogEntriesView(TemplateView):
    query_statistics_cases_body = "SELECT \
        logentry.id, \
        logentry.nationality,\
        COUNT(logentry.id) AS total, \
        sum(case when logentry.age > 0 AND logentry.age <= 5 Then 1 else 0 end) As age_0_5, \
        sum(case when logentry.age >= 6 AND logentry.age <= 9 Then 1 else 0 end) As age_6_9, \
        sum(case when logentry.age >= 10 AND logentry.age <= 14 Then 1 else 0 end) As age_10_14, \
        sum(case when logentry.age >= 15 AND logentry.age <= 17 Then 1 else 0 end) As age_15_17, \
        sum(case when logentry.age >= 18 AND logentry.age <= 24 Then 1 else 0 end) As age_18_24, \
        sum(case when logentry.age >= 25 AND logentry.age <= 49 Then 1 else 0 end) As age_25_49, \
        sum(case when logentry.age >= 50 AND logentry.age <= 59 Then 1 else 0 end) As age_50_59, \
        sum(case when logentry.age >= 60 Then 1 else 0 end) As age_gt60 \
    FROM caselog_logentry AS logentry"


    query_statistics_cases_totals_row = "UNION \
        SELECT \
            logentry.id, \
            \"TOTAL\", \
            COUNT(logentry.id) AS total, \
            sum(case when logentry.age > 0 AND logentry.age <= 5 Then 1 else 0 end) As age_0_5, \
            sum(case when logentry.age >= 6 AND logentry.age <= 9 Then 1 else 0 end) As age_6_9, \
            sum(case when logentry.age >= 10 AND logentry.age <= 14 Then 1 else 0 end) As age_10_14, \
            sum(case when logentry.age >= 15 AND logentry.age <= 17 Then 1 else 0 end) As age_15_17, \
            sum(case when logentry.age >= 18 AND logentry.age <= 24 Then 1 else 0 end) As age_18_24, \
            sum(case when logentry.age >= 25 AND logentry.age <= 49 Then 1 else 0 end) As age_25_49, \
            sum(case when logentry.age >= 50 AND logentry.age <= 59 Then 1 else 0 end) As age_50_59, \
            sum(case when logentry.age >= 60 Then 1 else 0 end) As age_gt60 \
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
        logentries = LogEntry.objects.filter(month__exact=1).prefetch_related('case')

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

        conselectedmonth = {
                    'logentries': logentries,
                    'month_form': month_form,
                    'months': self.months,
                    'nationalities': self.nationalities,
                    'newstats': rs_newstats,
                    'activestats': rs_activestats,
                    'selectedmonth': 'January',
                    }
        return render(request, self.template_name, conselectedmonth)


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
            
            conselectedmonth = {
                    'cases': self.cases,
                    'logentries': logentries,
                    'month_form': month_form,
                    'months': self.months,
                    'newstats': rs_newstats,
                    'activestats': rs_activestats,
                    'selectedmonth': selectedmonth,
                    }
            return render(request, self.template_name, conselectedmonth)
        else:
            messages.success(request, ('There was an error'))
        
            conselectedmonthAndRetriedvedFields = {
                    'cases': self.cases,
                    'month_form': month_form,
                    'months': self.months,
                    }
            return render(request, self.template_name, conselectedmonthAndRetriedvedFields)

    

class AddLogEntryView(TemplateView):
    template_name = 'caselog/add_logentry.html'
    cases = Case.objects.all()
    casetypes = LogEntry.CASETYPE
    casestatuses = LogEntry.CASESTATUS
    months = LogEntry.MONTH
    genders = LogEntry.GENDER
    nationalities = LogEntry.NATIONALITY
    psworkers = PsWorker.objects.all()

    def get(self, request):
        conselectedmonth = {
        'case': self.cases,
        'casetypes': self.casetypes,
        'casestatuses': self.casestatuses,
        'months': self.months,
        'genders': self.genders,
        'nationalities': self.nationalities,
        'psworkers': self.psworkers,
        }
        return render(request, self.template_name, conselectedmonth)

    def post(self, request):
        conselectedmonth = {
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
            

            # 1) create, fill, and save CaseObject then LogEntry Object            
            case_obj = Case(filenum= filenum)
            case_obj.save()
            
            logentry_obj = LogEntry(case=case_obj, casestatus= casestatus, month= month, casetype=casetype, age= age, fullname= fullname, gender=gender, nationality=nationlaity)
            logentry_obj.save()

            messages.success(request, ('Added Successfully'))
            return render(request, self.template_name, conselectedmonth)
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

            conselectedmonthAndRetriedvedFields = {
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
        return render(request, self.template_name, conselectedmonthAndRetriedvedFields)
            


def beneficiaries(request):
    rs_beneficiaries = getResultSet(query_beneficiaries)
    rs_statistics_new_all_benificiaries = getResultSet(query_statistics_new_all_benificiaries)
    rs_statistics_active_all_benificiaries = getResultSet(query_statistics_active_all_benificiaries)

    conselectedmonth = {
            'beneficiaries': rs_beneficiaries,
            'statistics_new_all_benificiaries': rs_statistics_new_all_benificiaries,
            'statistics_active_all_benificiaries': rs_statistics_active_all_benificiaries,
            }

    return render(request, 'caselog/beneficiaries.html', conselectedmonth)