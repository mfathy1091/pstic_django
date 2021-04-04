from django.urls import path
from . import views

urlpatterns = [

     path('addcase', views.AddCaseView.as_view(), name='caselog-addcase'),
     path('beneficiaries', views.beneficiaries, name='caselog-beneficiaries'),
     
     path('workers', views.PSWorkersView.as_view(), name='caselog-workers'),
     path('addworker', views.AddPsWorkerView.as_view(), name='caselog-addworker'),
     path('', views.PSWorkersView.as_view(), name='caselog-home'),
     path('case/<int:pk>', views.CaseDetail.as_view(), name='case-detail'),
     path('cases', views.CaseView.as_view(), name='caselog-cases'),

     path('monthlycases', views.LogEntriesView.as_view(), name='caselog-logentries'),
     path('addlogentry', views.AddLogEntryView.as_view(), name='caselog-addlogentry'),

     #path('cases', CaseView.as_view(template_name='caselog/cases.html'), name='caselog-cases'),
]
