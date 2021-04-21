from django.urls import path
from . import views

app_name = 'vehicle'

urlpatterns = [
    path('', views.VehicleList.as_view(), name='vehicle_list'),
    path('<int:pk>', views.VehicleDetail.as_view(), name='vehicle_detail'),
    path('create/', views.vehicle_create, name='vehicle_create'),
    #path('<int:pk>/<int:file_id>/', views.download, name='document_download'),
    #path('<int:pk>/<int:file_id>/delete', views.file_delete, name='file_delete'),
]
'''path('', views.home, name='home'),'''