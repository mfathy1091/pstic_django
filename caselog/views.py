from django.shortcuts import render, redirect
from django.views import View
from .models import PsWorker, Gender, Case, Nationality, Month, CaseType, DirectBenef, IndirectBenef
from django.db import connection
from .forms import PSWorkerForm, CaseForm, DirectBenefForm, MonthForm, CaseForm, PSWorkerForm, AddCaseForm
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView
from datetime import datetime
from .queries import Queries



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
            print(case_form.errors)
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



class AddMonthLog(TemplateView):
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
        selectedcase_obj = Case.objects.get(id=pk)
        selectedIndirectBenefs_qs = IndirectBenef.objects.filter(case_id__exact=pk)
        count = selectedIndirectBenefs_qs.count()


        context = {
                    'selectedcase': selectedcase_obj,
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