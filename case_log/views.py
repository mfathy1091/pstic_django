from django.shortcuts import render, redirect
from .models import workers, genders
from django.db import connection
from .forms import WorkerForm
from django.contrib import messages


query_workers = "SELECT \
        	w.id, \
            w.first_name, \
            w.last_name, \
            w.login_email, \
            w.login_password, \
            w.age, \
            g.gender_type, \
            j.job_title \
        FROM case_log_workers w \
        JOIN case_log_genders g ON w.gender_id_id = g.id \
        JOIN case_log_job_titles j ON j.id = w.job_title_id_id \
        ORDER BY w.id"

query_jobTitles = "SELECT * FROM case_log_job_titles"
query_genders = "SELECT * FROM case_log_genders"


def getResultSet(query):
    cursor = connection.cursor()
    cursor.execute(query)
    return cursor.fetchall()


def workers(request):
    rs_workers = getResultSet(query_workers)
    context = {'workers': rs_workers}
    return render(request, 'case_log/workers.html', context)


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
