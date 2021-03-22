from django.shortcuts import render, redirect
from .models import workers, genders, cases
from django.db import connection
from .forms import WorkerForm, CaseForm, BeneficiaryForm
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

# Queries

query_workers = "SELECT \
        	workers.id, \
            workers.fname, \
            workers.lname, \
            workers.login_email, \
            workers.login_password, \
            workers.age, \
            genders.gender, \
            job_titles.job_title, \
            workers.fname || ' ' || workers.lname AS 'full_name' \
        FROM case_log_workers workers \
        JOIN case_log_genders genders ON workers.gender_id_id = genders.id \
        JOIN case_log_job_titles job_titles ON job_titles.id = workers.job_title_id_id \
        ORDER BY workers.id"

query_cases = "SELECT \
        	cases.id, \
            cases.file_number, \
            months.month, \
            nationalities.nationality, \
            workers.fname || ' ' || workers.lname AS 'full_name', \
            caseStatues.case_status, \
            COUNT(beneficiaries.id) AS Beneficiaries \
        FROM case_log_cases AS cases \
        JOIN case_log_months months ON months.id = cases.month_id_id \
        JOIN case_log_workers workers ON workers.id = cases.worker_id_id \
        JOIN case_log_case_statuses caseStatues ON caseStatues.id = cases.case_status_id_id \
        JOIN case_log_nationalities nationalities ON nationalities.id = cases.nationality_id_id \
        LEFT JOIN case_log_beneficiaries beneficiaries ON cases.id = beneficiaries.case_id_id"

query_beneficiaries = "SELECT \
        	beneficiaries.id, \
            beneficiaries.full_name, \
            beneficiaries.age, \
            cases.file_number, \
            genders.gender, \
            beneficiaryStatuses.beneficiary_status \
        FROM case_log_beneficiaries beneficiaries \
        JOIN case_log_beneficiary_statuses beneficiaryStatuses ON beneficiaries.beneficiary_status_id_id = beneficiaryStatuses.id \
        JOIN case_log_genders genders ON beneficiaries.gender_id_id = genders.id \
        JOIN case_log_cases cases ON beneficiaries.case_id_id = cases.id"

query_jobTitles = "SELECT * FROM case_log_job_titles"
query_genders = "SELECT * FROM case_log_genders"
query_months = "SELECT * FROM case_log_months"
query_nationalities = "SELECT * FROM case_log_nationalities"
query_case_statuses = "SELECT * FROM case_log_case_statuses"
query_beneficiary_statuses = "SELECT * FROM case_log_beneficiary_statuses"

def getResultSet(query):
    cursor = connection.cursor()
    cursor.execute(query)
    return cursor.fetchall()


def workers(request):
    rs_workers = getResultSet(query_workers)
    context = {'workers': rs_workers}
    return render(request, 'case_log/workers.html', context)


def cases(request):
    query_beneficiaries_per_case = "SELECT \
        beneficiaries.id, \
        beneficiaries.full_name, \
        beneficiaries.age, \
        cases.file_number, \
        genders.gender, \
        beneficiary_statuses.beneficiary_status \
    FROM case_log_beneficiaries beneficiaries \
    JOIN case_log_beneficiary_statuses beneficiary_statuses ON beneficiaries.beneficiary_status_id_id = beneficiary_statuses.id \
    JOIN case_log_genders genders ON beneficiaries.gender_id_id = genders.id \
    JOIN case_log_cases cases ON beneficiaries.case_id_id = cases.id"
    
    rs_beneficiaries = getResultSet(query_beneficiaries_per_case)
    
    query_cases_odered = query_cases + \
        " GROUP BY cases.file_number, beneficiaries.case_id_id \
        ORDER BY cases.id"
    rs_cases = getResultSet(query_cases_odered)
    context = {
                'beneficiaries': rs_beneficiaries,
                'cases': rs_cases,
                }
    return render(request, 'case_log/cases.html', context)


def beneficiaries(request):
    rs_beneficiaries = getResultSet(query_beneficiaries)
    context = {'beneficiaries': rs_beneficiaries}
    return render(request, 'case_log/beneficiaries.html', context)

def add_worker(request):
    rs_workers = getResultSet(query_workers)
    rs_jobTitles = getResultSet(query_jobTitles)
    rs_genders = getResultSet(query_genders)

    if request.method == "POST":
        form = WorkerForm(request.POST or None)

        if form.is_valid():
            form.save()
            messages.success(request, ('Added Successfully'))
        else:
            first_name = request.POST['first_name']
            last_name = request.POST['last_name']
            login_email = request.POST['login_email']
            login_password = request.POST['login_password']
            age = request.POST['age']
            gender_id = request.POST['gender_id']
            job_title_id = request.POST['job_title_id']

            messages.success(request, ('There was an error'))

            tableAndFields = {
                    'workers': rs_workers,
                    'genders': rs_genders,
                    'jobTitles': rs_jobTitles,
                    'first_name': first_name,
                    'last_name': last_name,
                    'login_email': login_email,
                    'login_password': login_password,
                    'age': age,
                    'gender_id': gender_id,
                    'job_title_id': job_title_id,
            }
            return render(request, 'case_log/add_worker.html', tableAndFields)
        return redirect('caselog-workers')

        # redirect('case_log/workers.html')
    else:
        context = {
                'workers': rs_workers,
                'genders': rs_genders,
                'jobTitles': rs_jobTitles,
        }
        return render(request, 'case_log/add_worker.html', context)



def add_case(request):
    rs_cases = getResultSet(query_workers)
    rs_months = getResultSet(query_months)
    rs_nationalities = getResultSet(query_nationalities)
    rs_cases_statuses = getResultSet(query_case_statuses)
    
    # if submit button is pressed
    if request.method == "POST":
        form = CaseForm(request.POST or None)

        if form.is_valid():
            form.save()
            messages.success(request, ('Added Successfully'))
        else:
            file_number = request.POST['file_number']
            month_id = request.POST['month_id']
            worker_id = request.POST['worker_id']
            
            messages.success(request, ('There was an error'))

            #refill form data if failed to add a case
            tableAndFields = {
                'cases': rs_cases,
                'months': rs_months,
                'nationalities': rs_nationalities,
                'file_number': file_number,
                'month_id': month_id,
                'worker_id': worker_id,
            }
            return render(request, 'case_log/add_case.html', tableAndFields)
        return redirect('caselog-cases')

    # during adding filling the form
    else:
        context = {
                'workers': rs_cases,
                'months': rs_months,
                'nationalities': rs_nationalities,
                'cases_statuses': rs_cases_statuses,
        }
        return render(request, 'case_log/add_case.html', context)


def case_detail(request, pk):
    query_selectedCase = query_cases + " WHERE cases.id = " + str(pk)
    rs_selectedCase = getResultSet(query_selectedCase)
    rs_beneficiaryStatuses = getResultSet(query_beneficiary_statuses)
    rs_genders = getResultSet(query_genders)
    rs_cases = getResultSet(query_cases)
    query_caseSelectedBeneficiaries = query_beneficiaries + " WHERE cases.id = " + str(pk)
    rs_caseSelectedBeneficiaries = getResultSet(query_caseSelectedBeneficiaries)

    context = {
    'selectedCase': rs_selectedCase,
    'caseSelectedBeneficiaries': rs_caseSelectedBeneficiaries,
    'beneficiaryStatuses': rs_beneficiaryStatuses,
    'genders': rs_genders,
    'cases': rs_cases,
            }
    
    if request.method == "POST":
        form = BeneficiaryForm(request.POST or None)

        if form.is_valid():
            form.save()
            messages.success(request, ('Added Successfully'))
            temp = str(pk)
            return HttpResponseRedirect(temp)
        else:
            messages.success(request, ('There was an error'))
            return render(request, 'case_log/case_detail.html', context)
    else:
        return render(request, 'case_log/case_detail.html', context)


