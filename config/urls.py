from django.conf import settings
from django.conf.urls import include
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from crudmember import views as member_view

urlpatterns = [
    path('', include('homepage.urls')),
    path('service', member_view.Calendar.as_view(), name='home'),
    path('admin/', admin.site.urls),
    path('member/', include('crudmember.urls')),
    path('notice/', include('notice.urls')),
    path('dispatch/', include('dispatch.urls')),
    path('HR/', include('humanresource.urls')),
    path('vehicle/', include('vehicle.urls')),
    path('accounting/', include('accounting.urls')),
    path('document/', include('document.urls')),
    path('complaint/', include('complaint.urls')),
    path('assignment/', include('assignment.urls')),
    path('salary/', include('salary.urls')),
    path('approval/', include('approval.urls')),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += path('__debug__/', include('debug_toolbar.urls')),
