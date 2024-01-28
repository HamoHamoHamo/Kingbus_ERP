from django.urls import path
from . import views

app_name = 'HR'

urlpatterns = [
    path('member', views.MemberList.as_view(), name='member'),
    path('member/create', views.member_create, name='member_create'),
    path('member/edit', views.member_edit, name='member_edit'),
    path('member/delete', views.member_delete, name='member_delete'),
    path('member/file/upload', views.member_file_upload, name='member_file_upload'),
    path('member/file/<int:file_id>', views.member_file_download, name='member_file_download'),
    path('member/download', views.member_download, name='member_download'),
    #path('member/upload', views.member_upload, name='member_upload'),
    path('team', views.TeamList.as_view(), name='team'),
    path('team/create', views.team_create, name='team_create'),
    path('team/edit', views.team_edit, name='team_edit'),
    path('team/delete', views.team_delete, name='team_delete'),
    path('team/member', views.team_member, name='team_member'),
    path('salary', views.SalaryList.as_view(), name='salary'),
    path('salary/edit', views.salary_edit, name='salary_edit'),
    path('salary/detail', views.salary_detail, name='salary_detail'),
    path('salary/additional/create', views.salary_additional_create, name='salary_additional_create'),
    path('salary/additional/delete', views.salary_additional_delete, name='salary_additional_delete'),
    path('salary/deduction/create', views.salary_deduction_create, name='salary_deduction_create'),
    path('salary/deduction/delete', views.salary_deduction_delete, name='salary_deduction_delete'),
    path('salary/load', views.salary_load, name='salary_load'),
    # path('mgmt', views.ManagementList.as_view(), name='mgmt'),
    # path('mgmt/create', views.mgmt_create, name='mgmt_create'),

]