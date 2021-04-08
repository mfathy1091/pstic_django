from django.contrib import admin
import debug_toolbar
from django.conf import settings
from django.urls import include, path



urlpatterns = [
    path('admin/', admin.site.urls),
    # path('', include('login_portal.urls')),

    path('cashbox/', include('cash_box.urls')),
    path('caselog/', include('caselog.urls')),
    path('__debug__/', include(debug_toolbar.urls)),

    path('', include('accounts.urls')),


    ]


