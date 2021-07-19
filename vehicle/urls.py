from django.urls import path
from . import views

app_name = 'vehicle'

urlpatterns = [
    path('', views.VehicleList.as_view(), name='vehicle_list'),
    path('<int:pk>', views.vehicle_detail, name='vehicle_detail'),  # update랑 같이있음
    path('create/', views.vehicle_create, name='vehicle_create'),
    path('<int:pk>/delete', views.vehicle_delete, name='vehicle_delete'),
    path('<int:vehicle_id>/<int:file_id>', views.download, name='vehicle_file_download'),
    path('<int:vehicle_id>/<int:file_id>/file_del', views.vehicle_file_del, name='vehicle_file_del'),
    # path('<int:pk>/<int:file_id>/', views.download, name='document_download'),
    # path('<int:pk>/<int:file_id>/delete', views.file_delete, name='file_delete'),
]
'''path('', views.home, name='home'),'''
