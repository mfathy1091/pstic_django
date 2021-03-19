from django.shortcuts import render, redirect
from .models import workers, genders, cases
from django.db import connection
from .forms import WorkerForm, CaseForm
from django.contrib import messages

from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

# Queries

query_workers = "SELECT \
        	w.id, \
            w.first_name, \
            w.last_name, \
            w.login_email, \
            w.login_password, \
            w.age, \
            g.gender_type, \
            j.job_title, \
            w.first_name || ' ' || w.last_name AS 'full_name' \
        FROM case_log_workers w \
        JOIN case_log_genders g ON w.gender_id_id = g.id \
        JOIN case_log_job_titles j ON j.id = w.job_title_id_id \
        ORDER BY w.id"

query_cases = "SELECT \
        	c.id, \
            c.file_number, \
            m.month, \
            w.first_name || ' ' || w.last_name AS 'full_name', \
            cs.case_status \
        FROM case_log_cases c \
        JOIN case_log_months m ON m.id = c.month_id_id \
        JOIN case_log_workers w ON w.id = c.worker_id_id \
        JOIN case_log_case_statuses cs ON cs.id = c.case_status_id_id \
        ORDER BY c.id"

query_beneficiaries = "SELECT \
        	b.id, \
            b.full_name, \
            b.age, \
            c.file_number, \
            g.gender_type, \
            bs.beneficiary_status \
        FROM case_log_beneficiaries b \
        JOIN case_log_beneficiary_statuses bs ON b.beneficiary_status_id_id = bs.id \
        JOIN case_log_genders g ON b.gender_id_id = g.id \
        JOIN case_log_cases c ON b.file_number_id_id = c.id \
        ORDER BY b.id"

query_jobTitles = "SELECT * FROM case_log_job_titles"
query_genders = "SELECT * FROM case_log_genders"
query_months = "SELECT * FROM case_log_months"
query_case_statuses = "SELECT * FROM case_log_case_statuses"



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
        b.id, \
        b.full_name, \
        b.age, \
        c.file_number, \
        g.gender_type, \
        bs.beneficiary_status \
    FROM case_log_beneficiaries b \
    JOIN case_log_beneficiary_statuses bs ON b.beneficiary_status_id_id = bs.id \
    JOIN case_log_genders g ON b.gender_id_id = g.id \
    JOIN case_log_cases c ON b.file_number_id_id = c.id"
    
    #WHERE c.id = " + str(pk)

    rs_beneficiaries = getResultSet(query_beneficiaries_per_case)
    
    rs_cases = getResultSet(query_cases)
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
        tables = {
                'workers': rs_workers,
                'genders': rs_genders,
                'jobTitles': rs_jobTitles,
        }
        return render(request, 'case_log/add_worker.html', tables)



def add_case(request):
    rs_cases = getResultSet(query_workers)
    rs_months = getResultSet(query_months)
    rs_cases_statuses = getResultSet(query_case_statuses)
    

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
                'file_number': file_number,
                'month_id': month_id,
                'worker_id': worker_id,
            }
            return render(request, 'case_log/add_case.html', tableAndFields)
        return redirect('caselog-cases')


        # redirect('case_log/workers.html')
    else:
        tables = {
                'workers': rs_cases,
                'months': rs_months,
                'cases_statuses': rs_cases_statuses,
        }
        return render(request, 'case_log/add_case.html', tables)




def home2 (request):
    all_workers = Workers.objects.all
    return render(request, 'case_log/home.html', {'workers': all_workers})


postsList = [
    {
        'author': 'CoreyMS',
        'title': 'Blog Post 1',
        'content': 'First post content',
        'date_posted': 'August 27, 2018'
    },
    {
        'author': 'Jane Doe',
        'title': 'Blog Post 2',
        'content': 'Second post content',
        'date_posted': 'August 28, 2018'
    }
]



def case_detail(request, pk):

    query_selectedCase = "SELECT \
        	c.id, \
            c.file_number, \
            m.month, \
            w.first_name || ' ' || w.last_name AS 'full_name', \
            cs.case_status \
        FROM case_log_cases c \
        JOIN case_log_months m ON m.id = c.month_id_id \
        JOIN case_log_workers w ON w.id = c.worker_id_id \
        JOIN case_log_case_statuses cs ON cs.id = c.case_status_id_id \
        WHERE c.id = " + str(pk)

    query_caseSelectedBeneficiaries = "SELECT \
        	b.id, \
            b.full_name, \
            b.age, \
            c.file_number, \
            g.gender_type, \
            bs.beneficiary_status \
        FROM case_log_beneficiaries b \
        JOIN case_log_beneficiary_statuses bs ON b.beneficiary_status_id_id = bs.id \
        JOIN case_log_genders g ON b.gender_id_id = g.id \
        JOIN case_log_cases c ON b.file_number_id_id = c.id \
        WHERE c.id = " + str(pk)

    rs_selectedCase = getResultSet(query_selectedCase)
    rs_caseSelectedBeneficiaries = getResultSet(query_caseSelectedBeneficiaries)
    
    context = {
        'selectedCase': rs_selectedCase,
        'caseSelectedBeneficiaries': rs_caseSelectedBeneficiaries,
                }
    return render(request, 'case_log/case_detail.html', context)


