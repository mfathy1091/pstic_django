from django.urls import path
from . import views

urlpatterns = [
     path('', views.workers, name='caselog-home'),
     path('workers', views.workers, name='caselog-workers'),
     path('addworker', views.add_worker, name='caselog-addworker'),
]
