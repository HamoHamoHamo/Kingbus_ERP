from django.urls import path
from . import views

app_name = 'HR'

urlpatterns = [
    path('member', views.MemberList.as_view(), name='member'),
    path('member/create', views.member_create, name='member_create'),
    path('member/edit', views.member_edit, name='member_edit'),
    path('member/delete', views.member_delete, name='member_delete'),
    path('salary', views.SalaryList.as_view(), name='salary'),
    path('salary/detail', views.salary_detail, name='salary_detail'),
    # path('mgmt', views.ManagementList.as_view(), name='mgmt'),
    # path('mgmt/create', views.mgmt_create, name='mgmt_create'),

]