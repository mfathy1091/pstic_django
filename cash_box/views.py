from django.shortcuts import render

def home (request):
    return render(request, 'cash_box/home.html')
