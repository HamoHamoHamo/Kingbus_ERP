from django.urls import path
from . import views

app_name = 'accounting'

urlpatterns = [
    path('salary', views.SalaryList.as_view(), name='salary'),
    path('salary/<int:pk>', views.SalaryDetail.as_view(), name='salary_detail'),
    path('salary/create', views.salary_create, name='salary_create'),
    path('salary/edit', views.salary_edit, name='salary_edit'),
    path('salary/delete', views.salary_delete, name='salary_delete'),
    path('salary/remark/edit', views.remark_edit, name='remark_edit'),
    path('income', views.IncomeList.as_view(), name='income'),
    
    path('collect', views.CollectList.as_view(), name='collect'),
    path('collect/create', views.collect_create, name='collect_create'),
    path('collect/delete', views.collect_delete, name='collect_delete'),
    path('collect/load', views.collect_load, name='collect_load'),
    path('collect/additional/create', views.additional_collect_create, name='additional_collect_create'),
    path('collect/additional/delete', views.additional_collect_delete, name='additional_collect_delete'),
    
    path('regularly/collect', views.RegularlyCollectList.as_view(), name='regularly_collect'),
    path('regularly/collect/create', views.r_collect_create, name='r_collect_create'),
    path('regularly/collect/additional/create', views.r_additional_collect_create, name='r_additional_collect_create'),
    path('regularly/collect/additional/delete', views.r_additional_collect_delete, name='r_additional_collect_delete'),
    path('regularly/load', views.regularly_load, name='regularly_load'),
    
    path('deposit', views.DepositList.as_view(), name='deposit'),
    path('deposit/data', views.load_deposit_data, name='load_deposit_data'),
    path('deposit/create', views.deposit_create, name='deposit_create'),
    path('deposit/edit', views.deposit_edit, name='deposit_edit'),
    path('deposit/hide', views.deposit_hide, name='deposit_hide'),
]
