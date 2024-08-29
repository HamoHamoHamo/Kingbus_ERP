from django.urls import path
from . import views

app_name = 'approval'

urlpatterns = [
    path('', views.ApprovalList.as_view(), name="approval"),
    path('detail/<int:pk>', views.ApprovalDetail.as_view(), name="approval_detail"),
    path('process', views.ApprovalProcess.as_view(), name="approval_process"),
    path('create', views.approval_create, name="approval_create"),
    path('edit', views.approval_edit, name="approval_edit"),
    path('delete', views.approval_delete, name="approval_delete"),
    path('approver/create', views.approver_create, name="approver_create"),
    path('approver/create', views.approver_create, name="approver_create"),
    path('approver/edit', views.approver_edit, name="approver_edit"),


]