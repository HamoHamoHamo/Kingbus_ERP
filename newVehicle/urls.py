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


    # path('maintenance/<int:vehicle_id>/', views.maintenance_view, name='maintenance_view'),  # 차량 ID를 URL로 전달
    # path('maintenance/create', views.maintenance_create, name='maintenance_create')
]