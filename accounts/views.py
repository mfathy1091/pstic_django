from django.shortcuts import render
from django.http import HttpResponse


def home(request):
    return HttpResponse('Home page')

def products(request):
    return HttpResponse('products')

def customer(request):
    return HttpResponse('customer')
