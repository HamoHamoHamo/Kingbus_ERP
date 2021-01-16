from django.conf import settings
from django.conf.urls import include
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path
from crudmember import views as member_view

urlpatterns = [
    path('', member_view.home, name='home'),
    path('admin/', admin.site.urls),
    path('member/', include('crudmember.urls')),
    path('notice/', include('notice.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)