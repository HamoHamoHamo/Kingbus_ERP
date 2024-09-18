from django.urls import path
from . import views

app_name = 'approval'

urlpatterns = [
    path('', views.ApprovalList.as_view(), name="approval"),
    path('detail/<int:pk>', views.ApprovalDetail.as_view(), name="approval_detail"),
    path('edit/<int:pk>', views.ApprovalEdit.as_view(), name="approval_edit"),
    path('create', views.approval_create, name="approval_create"),
    path('delete', views.approval_delete, name="approval_delete"),
    path('approver/edit', views.approver_edit, name="approver_edit"),
    path('file/<int:file_id>', views.approval_file_download, name='approval_file_download'),
    path('file/<int:file_id>/delete', views.approval_file_delete, name='approval_file_delete'),

]