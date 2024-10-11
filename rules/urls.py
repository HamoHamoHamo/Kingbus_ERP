from django.urls import path
from . import views

appname= 'rules'

urlpatterns = [
    path('approvalrules', views.ApprovalRules.as_view(), name='approvalrules'),
    path('rowcallrules', views.RowCallRules.as_view(), name='rowcallrules'),
    path('driverrules', views.DriverRules.as_view(), name='driverrules'),
    path('managerrules', views.ManagerRules.as_view(), name='managerrules'),
    path('fieldmanagerrules', views.FieldManagerRules.as_view(), name='fieldmanagerrules'),
    path('personnelcommittee', views.PersonnelCommittee.as_view(), name='personnelcommittee'),
    path('Itemmanagement', views.ItemManagement.as_view(), name='Itemmanagement'),
    path('organizationchart', views.OrganizationChart.as_view(), name='organizationchart'),
]