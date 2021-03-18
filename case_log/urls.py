from django.urls import path
from . import views

urlpatterns = [
     path('', views.workers, name='caselog-home'),
     path('workers', views.workers, name='caselog-workers'),
     path('addworker', views.add_worker, name='caselog-addworker'),
     path('cases', views.cases, name='caselog-cases'),
     path('addcase', views.add_case, name='caselog-addcase'),
     path('beneficiaries', views.beneficiaries, name='caselog-beneficiaries'),
     path('case/<int:pk>', views.case_detail, name='case-detail'),
]
