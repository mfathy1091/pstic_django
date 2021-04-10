from django.urls import path
from . import views

urlpatterns = [

     path('addcase', views.AddCaseView.as_view(), name='caselog-addcase'),
     path('beneficiaries', views.beneficiaries, name='caselog-beneficiaries'),
     
     path('workers', views.PSWorkersView.as_view(), name='caselog-workers'),
     path('addworker', views.AddPsWorkerView.as_view(), name='caselog-addworker'),
     
     #path('', views.PSWorkersView.as_view(), name='caselog-home'),
     path('case/<int:pk>', views.CaseDetail.as_view(), name='case-detail'),
     path('cases', views.CaseView.as_view(), name='caselog-cases'),

     path('monthlycases', views.LogEntriesView.as_view(), name='caselog-logentries'),
     path('addlogentry', views.AddLogEntry.as_view(), name='caselog-addlogentry'),
     path('updatelogentry/<str:pk>', views.UpdateLogEntry.as_view(), name='caselog-updatelogentry'),
     
     #path('cases', CaseView.as_view(template_name='caselog/cases.html'), name='caselog-cases'),
     path('', views.Dashboard.as_view(), name='caselog-dashboard'),
     path('caselog/psworker/<str:pk_test>/', views.PsWorkerView.as_view(), name="psworker"),
]
