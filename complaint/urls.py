from django.urls import path
from . import views

app_name = 'complaint'

urlpatterns = [
    path('consulting', views.ConsultingList.as_view(), name='consulting'),
    path('consulting/edit', views.consulting_edit, name='consulting_edit'),
    path('consulting/delete', views.consulting_delete, name='consulting_delete'),
    path('consulting/img/<int:id>', views.consulting_image, name='consulting_img'),
    path('inspection', views.InspectionList.as_view(), name='inspection'),
    path('inspection/edit', views.inspection_edit, name='inspection_edit'),
    path('inspection/delete', views.inspection_delete, name='inspection_delete'),
    path('inspection/img/<int:id>', views.inspection_image, name='inspection_img'),
    path('grievance', views.Grievance.as_view(), name='grievance'),
]
