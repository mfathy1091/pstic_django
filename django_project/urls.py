from django.contrib import admin
import debug_toolbar
from django.conf import settings
from django.urls import include, path

from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),
    # path('', include('login_portal.urls')),

    path('cashbox/', include('cash_box.urls')),
    path('', include('caselog.urls')),
    path('__debug__/', include(debug_toolbar.urls)),

    #path('', include('accounts.urls')),


    ]


urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)