from django.urls import path
from . import views

app_name = 'assignment'

urlpatterns = [
    path('', views.AssignmentList.as_view(), name="assignment"),
    path('temporary', views.TemporaryAssignmentList.as_view(), name="temporary_assignment"),
    path('temporary/create', views.temporary_assignment_create, name="temporary_assignment_create"),
    path('temporary/edit', views.temporary_assignment_edit, name="temporary_assignment_edit"),
    # path('temporary/edit/check', views.assignment_edit_check, name="temporary_assignment_edit_check"),
    path('temporary/connect/delete', views.temporary_connect_delete, name="temporary_connect_delete"),
    path('temporary/delete', views.temporary_assignment_delete, name="temporary_assignment_delete"),
    path('data', views.AssignmentDataList.as_view(), name="assignment_data"),
    path('create', views.assignment_create, name="assignment_create"),
    path('edit', views.assignment_edit, name="assignment_edit"),
    path('edit/check', views.assignment_edit_check, name="assignment_edit_check"),
    path('delete', views.assignment_delete, name="assignment_delete"),
    path('connect/create', views.connect_create, name="connect_create"),
    path('connect/delete', views.connect_delete, name="connect_delete"),
    path('group/create', views.group_create, name="group_create"),
    path('group/edit', views.group_edit, name="group_edit"),
    path('group/delete', views.group_delete, name="group_delete"),
    path('group/fix', views.group_fix, name="group_fix"),

    path('approval', views.Approval.as_view(), name="approval"),
    path('approval_process', views.ApprovalProcess.as_view(), name="approval_process")
]
