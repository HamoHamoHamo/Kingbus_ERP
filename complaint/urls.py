from django.urls import path
from . import views

app_name = 'complaint'

urlpatterns = [
    path('consulting', views.ConsultingList.as_view(), name='consulting'),
    path('consulting/edit', views.consulting_edit, name='consulting_edit'),
    path('consulting/delete', views.consulting_delete, name='consulting_delete'),
    path('maintance', views.MaintanceList.as_view(), name='vehicle_inspection'),
]
