from django.urls import path
from . import views

urlpatterns = [

     path('addcase', views.AddCaseView.as_view(), name='addcase'),
     path('beneficiaries', views.beneficiaries, name='beneficiaries'),
     
     path('workers', views.PSWorkersView.as_view(), name='workers'),
     path('addworker', views.AddPsWorkerView.as_view(), name='addworker'),
     
     
     path('cases', views.CaseView.as_view(), name='cases'),

     path('monthlycases', views.LogEntriesView.as_view(), name='logentries'),
     path('addlogentry', views.AddLogEntry.as_view(), name='addlogentry'),
     
     #path('cases', CaseView.as_view(template_name='caselog/cases.html'), name='caselog-cases'),
     path('', views.Dashboard.as_view(), name='dashboard'),
     path('caselog/psworker/<str:pk_test>/', views.PsWorkerView.as_view(), name="psworker"),
     path('createlogentry/<str:workerpk>/', views.CreateLogEntry.as_view(), name='createlogentry'),
     path('updatelogentry/<str:pk>/', views.updateLogEntry, name='updatelogentry'),
     path('deletelogentry/<str:pk>/', views.deleteLogEntry, name='deletelogentry'),


     path('register/', views.registerPage, name='register'),
     path('login/', views.loginPage, name='login'),
     path('logout/', views.logoutUser, name='logout'),
     path('user/', views.UserPage.as_view(), name='user-page'),
     path('account/', views.accountSettings, name="account"),

     path('case/<str:entrypk>', views.CaseDetail.as_view(), name='case-detail'),
     path('addvisit/<str:entrypk>/', views.AddVisit.as_view(), name='addvisit'),


]
