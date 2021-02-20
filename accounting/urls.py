from django.urls import path
from . import views

app_name = 'accounting'

urlpatterns = [
    path('outlay/', views.OutlayList.as_view(), name='outlay_list'),
    path('outlay/create/', views.outlay_create, name='outlay_create'),
    path('outlay/<int:pk>/', views.OutlayDetail.as_view(), name='outlay_detail'),
    path('outlay/<int:pk>/delete/', views.outlay_delete, name='outlay_delete'),
    path('outlay/<int:pk>/edit/', views.outlay_edit, name='outlay_edit'),
    
    path('outlay/salary/', views.SalaryList.as_view(), name='salary_list'),
    path('outlay/salary/create/', views.salary_create, name='salary_create'),
    path('outlay/salary/<int:pk>/', views.SalaryDetail.as_view(), name='salary_detail'),
    path('outlay/salary/<int:pk>/delete/', views.salary_delete, name='salary_delete'),
    path('outlay/salary/<int:pk>/edit/', views.salary_edit, name='salary_edit'),


    path('income/', views.IncomeList.as_view(), name='income_list'),
    path('income/create/', views.income_create, name='income_create'),
    path('income/<int:pk>/', views.IncomeDetail.as_view(), name='income_detail'),
    path('income/<int:pk>/delete/', views.income_delete, name='income_delete'),
    path('income/<int:pk>/edit/', views.income_edit, name='income_edit'),

    path('income/collect/', views.CollectList.as_view(), name='collect_list'),
    path('income/collect/<int:pk>/', views.CollectDetail.as_view(), name='collect_detail'),
    path('income/collect/<int:pk>/edit', views.collect_edit, name='collect_edit'),
]
