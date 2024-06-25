from django.urls import path
from . import views

app_name = 'salary'

urlpatterns = [
    path('status', views.SalaryStatus.as_view(), name="status"),
    path('table', views.SalaryTable.as_view(), name="table"),
    path('hourlywage/save', views.HourlyWageSaveView.as_view(), name="hourly_wage_save")
]