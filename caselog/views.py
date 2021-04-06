from django.shortcuts import render, redirect
from django.views import View
from .models import PsWorker, Gender, Case, Nationality, Month, CaseType, CaseStatus, IndirectBenef, LogEntry
from django.db import connection
from .forms import PSWorkerForm, CaseForm, FilterByMonthForm, MonthForm, CaseForm, PSWorkerForm, AddCaseForm, AddLogEntryForm
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


class AddPsWorkerView(TemplateView):
    template_name = 'caselog/add_worker.html'
    psworkers = PsWorker.objects.all()
    genders = Gender.objects.all()
    nationalities = Nationality.objects.all()

    def get(self, request):
        #  define a blank form to render it
        #addpsworker_form = PSWorkerForm()

        context = {
        'psworkers': self.psworkers,
        'genders': self.genders,
        'nationalities': self.nationalities,
        #'addpsworker_form':addpsworker_form,
        }
        return render(request, self.template_name, context)
    
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
            #text = addpsworker_form.cleaned_data['fullname']
            #addpsworker_form = PSWorkerForm(request.POST) # refills the form if you instatioated the form naem in html form tag and removed the hard coded form
            
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
                }
            return render(request, self.template_name, contextAndRetriedvedFields)

class AddCaseView(TemplateView):
    template_name = 'caselog/add_case.html'
    cases = Case.objects.all()
    casetypes = CaseType.objects.all()
    months = Month.objects.all()
    genders = Gender.objects.all()
    nationalities = Nationality.objects.all()
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



class AddLogEntry(TemplateView):
    template_name = 'caselog/add_worker.html'
    psworkers = PsWorker.objects.all()
    genders = Gender.objects.all()
    nationalities = Nationality.objects.all()

    def get(self, request):
        #  define a blank form to render it
        #addpsworker_form = PSWorkerForm()

        context = {
        'psworkers': self.psworkers,
        'genders': self.genders,
        'nationalities': self.nationalities,
        #'addpsworker_form':addpsworker_form,
        }
        return render(request, self.template_name, context)
    
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
            #text = addpsworker_form.cleaned_data['fullname']
            #addpsworker_form = PSWorkerForm(request.POST) # refills the form if you instatioated the form naem in html form tag and removed the hard coded form
            
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
    months = Month.objects.all()

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
            text = month_form.cleaned_data['month']
            #month_form = MonthForm() # to balnk the form

        context = {
                    'cases': self.cases,
                    'month_form': month_form,
                    'text': text,
                    'months': self.months,
                    }
        return render(request, self.template_name, context)


        
    
class LogEntriesView(TemplateView):
    query_statistics_cases_body = "SELECT \
        logentry.id, \
        nationality.name AS nation,\
        COUNT(logentry.id) AS total, \
        sum(case when logentry.dage > 0 AND logentry.dage <= 5 Then 1 else 0 end) As age_0_5, \
        sum(case when logentry.dage >= 6 AND logentry.dage <= 9 Then 1 else 0 end) As age_6_9, \
        sum(case when logentry.dage >= 10 AND logentry.dage <= 14 Then 1 else 0 end) As age_10_14, \
        sum(case when logentry.dage >= 15 AND logentry.dage <= 17 Then 1 else 0 end) As age_15_17, \
        sum(case when logentry.dage >= 18 AND logentry.dage <= 24 Then 1 else 0 end) As age_18_24, \
        sum(case when logentry.dage >= 25 AND logentry.dage <= 49 Then 1 else 0 end) As age_25_49, \
        sum(case when logentry.dage >= 50 AND logentry.dage <= 59 Then 1 else 0 end) As age_50_59, \
        sum(case when logentry.dage >= 60 Then 1 else 0 end) As age_gt60 \
    FROM caselog_logentry AS logentry \
    JOIN caselog_month month ON month.id = logentry.month_id \
    JOIN caselog_nationality nationality ON nationality.id = logentry.dnationality_id"


    query_statistics_cases_totals_row = "UNION \
        SELECT \
            logentry.id, \
            \"TOTAL\", \
            COUNT(logentry.id) AS total, \
            sum(case when logentry.dage > 0 AND logentry.dage <= 5 Then 1 else 0 end) As age_0_5, \
            sum(case when logentry.dage >= 6 AND logentry.dage <= 9 Then 1 else 0 end) As age_6_9, \
            sum(case when logentry.dage >= 10 AND logentry.dage <= 14 Then 1 else 0 end) As age_10_14, \
            sum(case when logentry.dage >= 15 AND logentry.dage <= 17 Then 1 else 0 end) As age_15_17, \
            sum(case when logentry.dage >= 18 AND logentry.dage <= 24 Then 1 else 0 end) As age_18_24, \
            sum(case when logentry.dage >= 25 AND logentry.dage <= 49 Then 1 else 0 end) As age_25_49, \
            sum(case when logentry.dage >= 50 AND logentry.dage <= 59 Then 1 else 0 end) As age_50_59, \
            sum(case when logentry.dage >= 60 Then 1 else 0 end) As age_gt60 \
        FROM caselog_logentry AS logentry \
        JOIN caselog_month month ON month.id = logentry.month_id \
        JOIN caselog_nationality nationality ON nationality.id = logentry.dnationality_id"



    template_name = 'caselog/logentries.html'
    logentries = LogEntry.objects.prefetch_related('month', 'case', 'casestatus', 'casetype', 'dgender', 'dnationality')
    cases = Case.objects.all().prefetch_related()
    months = Month.objects.all()
    nationalities = Nationality.objects.all()
    

    def getstats(self):
        nationalities = Nationality.objects.all()
        for nation in nationalities:
            logentries_per_nation = self.logentries.filter(dnationality__exact=nation)
            total_per_nation = logentries_per_nation.count()
            total_ages_0_5 = logentries_per_nation.filter(dage__gte=0).filter(dage__lte=5).count()
            total_ages_6_9 = logentries_per_nation.filter(dage__gte=6).filter(dage__lte=9).count()
            total_ages_10_14 = logentries_per_nation.filter(dage__gte=10).filter(dage__lte=14).count()
            total_ages_15_17 = logentries_per_nation.filter(dage__gte=15).filter(dage__lte=17).count()
            total_ages_18_24 = logentries_per_nation.filter(dage__gte=18).filter(dage__lte=24).count()
            total_ages_25_49 = logentries_per_nation.filter(dage__gte=25).filter(dage__lte=49).count()
            total_ages_50_59 = logentries_per_nation.filter(dage__gte=50).filter(dage__lte=59).count()
            total_ages_gt_60 = logentries_per_nation.filter(dage__gte=60).count()

            
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
        logentries = LogEntry.objects.filter(month__exact=1).prefetch_related('month', 'case', 'casestatus', 'casetype', 'dgender', 'dnationality')

        query_statistics_new_cases = self.query_statistics_cases_body + " WHERE \
            logentry.month_id = 1 AND logentry.casestatus_id = 1 \
            GROUP BY nation " + self.query_statistics_cases_totals_row + " WHERE \
            logentry.month_id = 1 AND logentry.casestatus_id = 1"

        query_statistics_active_cases = self.query_statistics_cases_body + " WHERE \
            logentry.month_id = 1 AND (logentry.casestatus_id = 1 OR logentry.casestatus_id = 2) \
            GROUP BY nation " + self.query_statistics_cases_totals_row + " WHERE \
            logentry.month_id = 1 AND (logentry.casestatus_id = 1 OR logentry.casestatus_id = 2)"

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
            text = month_form.cleaned_data['month']
            logentries = LogEntry.objects.filter(month__exact=text).prefetch_related('month', 'case', 'casestatus', 'casetype', 'dgender', 'dnationality')

            query_statistics_new_cases = self.query_statistics_cases_body + " WHERE \
                logentry.month_id = " + text + " AND logentry.casestatus_id = 1 \
                GROUP BY nation " + self.query_statistics_cases_totals_row + " WHERE \
                logentry.month_id = " + text + " AND logentry.casestatus_id = 1"

            query_statistics_active_cases = self.query_statistics_cases_body + " WHERE \
                logentry.month_id = " + text + " AND (logentry.casestatus_id = 1 OR logentry.casestatus_id = 2) \
                GROUP BY nation " + self.query_statistics_cases_totals_row + " WHERE \
                logentry.month_id = " + text + " AND (logentry.casestatus_id = 1 OR logentry.casestatus_id = 2)"

            rs_newstats = LogEntry.objects.raw(query_statistics_new_cases)
            rs_activestats = LogEntry.objects.raw(query_statistics_active_cases)
            
            rs_selectedmonth = Month.objects.filter(id__exact=text).get()
            context = {
                    'cases': self.cases,
                    'logentries': logentries,
                    'month_form': month_form,
                    'months': self.months,
                    'newstats': rs_newstats,
                    'activestats': rs_activestats,
                    'selectedmonth': rs_selectedmonth,
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

    

class AddLogEntryView(TemplateView):
    template_name = 'caselog/add_logentry.html'
    cases = Case.objects.all()
    casetypes = CaseType.objects.all()
    casestatuses = CaseStatus.objects.all()
    months = Month.objects.all()
    genders = Gender.objects.all()
    nationalities = Nationality.objects.all()
    psworkers = PsWorker.objects.all()

    def get(self, request):
        context = {
        'case': self.cases,
        'casetypes': self.casetypes,
        'casestatuses': self.casestatuses,
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
            month_obj = Month.objects.filter(id__exact=form.cleaned_data['month']).get()
            casestatus_obj = CaseStatus.objects.filter(id__exact=form.cleaned_data['casestatus']).get()
            casetype_obj = CaseType.objects.filter(id__exact=form.cleaned_data['casetype']).get()
            gender_obj = Gender.objects.filter(id__exact=form.cleaned_data['gender']).get()
            nationality_obj = Nationality.objects.filter(id__exact=form.cleaned_data['nationality']).get()
            

            # get values from input fields
            fullname = form.cleaned_data.get('fullname')
            filenum = form.cleaned_data['filenum']
            age = form.cleaned_data['age']

            # 1) create, fill, and save CaseObject then LogEntry Object            
            case_obj = Case(filenum= filenum)
            case_obj.save()
            
            logentry_obj = LogEntry(case=case_obj, casestatus= casestatus_obj, month= month_obj, casetype=casetype_obj, dage= age, dfullname= fullname, dgender=gender_obj, dnationality=nationality_obj)
            logentry_obj.save()

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
            