from django.urls import path
from . import views

app_name = 'vehicle'

urlpatterns = [
    path('list', views.VehicleList.as_view(), name='list'),
    path('list/create', views.vehicle_create, name='vehicle_create'),
    path('list/edit', views.vehicle_edit, name='vehicle_edit'),
    path('list/delete', views.vehicle_delete, name='vehicle_delete'),
    path('list/download', views.vehicle_download, name='vehicle_download'),
	path('list/upload', views.vehicle_upload, name='vehicle_upload'),
    path('photo/create', views.photo_file_create, name='photo_file_create'),
    path('photo/delete', views.photo_file_delete, name='photo_file_delete'),
    path('photo/list', views.photo_list, name='photo_list'),
    path('photo/image/<int:file_id>', views.PhotoImageViewer.as_view(), name='vehicle_photo_image'),
    path('document/image/<int:file_id>', views.DocumentImageViewer.as_view(), name='vehicle_document_image'),
    path('document/upload', views.document_file_upload, name='document_file_upload'),
    path('maintenance/create', views.maintenance_create, name='maintenance_create'),
    path('maintenance/list', views.maintenance_list, name='maintenance_list'),
    path('maintenance/delete', views.maintenance_delete, name='maintenance_delete'),
    path('efficiency', views.efficiency, name='efficiency'),
    path('refueling', views.RefuelingList.as_view(), name='refueling'),
    path('refueling/delete', views.refueling_delete, name='refueling_delete'),
    # path('maintenance', views.MaintenanceList.as_view(), name='maintenance'),
    path('accident', views.AccidentList.as_view(), name='accident'),
    path('dailychecklist', views.DailyChecklistListView.as_view(), name='dailychecklist'),
    path('weeklychecklist', views.WeeklyChecklistListView.as_view(), name='weeklychecklist'),
    path('equipmentchecklist', views.EquipmentChecklistListView.as_view(), name='equipmentchecklist'),

    # path('mgmt', views.VehicleMgmt.as_view(), name='mgmt'),
    # path('mgmt/insurance/edit', views.insurance_edit, name='insurance_edit'),
    # path('mgmt/check/edit', views.check_edit, name='check_edit'),
    # path('', views.VehicleList.as_view(), name='vehicle_list'),
    # path('create/', views.vehicle_create, name='vehicle_create'),
    # path('delete/', views.vehicle_delete, name='vehicle_delete'),
    # path('<int:pk>/', views.VehicleDetail.as_view(), name='vehicle_detail'),  # update랑 같이있음
    # path('<int:pk>/edit/', views.vehicle_edit, name='vehicle_edit'),
    # path('<int:vehicle_id>/<int:file_id>/', views.download, name='file_download'),
    # path('<int:vehicle_id>/<int:file_id>/file_del/', views.vehicle_file_del, name='file_del'),
    #     # path('<int:pk>/<int:file_id>/', views.download, name='document_download'),
    #     # path('<int:pk>/<int:file_id>/delete', views.file_delete, name='file_delete'),
]
'''path('', views.home, name='home'),'''
