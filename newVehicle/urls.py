from django.urls import path
from . import views


app_name = 'newVehicle'

urlpatterns = [
    path('list', views.VehicleListView.as_view(), name='vehicle_view'),
    path('list/create', views.vehicle_create, name='vehicle_create'),
    path('list/update/<int:pk>', views.vehicle_update, name='vehicle_update'),
    path('list/delete', views.vehicle_delete_multiple, name='vehicle_delete_multiple'),
    path('list/download', views.vehicle_download, name='vehicle_download'),  # 엑셀 다운로드
    path('list/upload', views.vehicle_excel_upload, name='vehicle_excel_upload'),  # 엑셀 업로드 URL 추가

    # path('vehicle/<int:vehicle_id>/maintenance_create', views.maintenance_create, name='maintenance_create'), # 정비 내역 추가 URL
    # # path('vehicle/<int:maintenance_id>/<int:vehicle_id>/maintenance_delete', views.maintenance_delete, name='maintenance_delete'),
    # path('maintenance/delete_multiple', views.maintenance_delete_multiple, name='maintenance_delete_multiple'),

    path('vehicle/<int:vehicle_id>/maintenance_create_or_delete', views.maintenance_create_or_delete, name='maintenance_create_or_delete'),
]