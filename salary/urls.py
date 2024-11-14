from django.urls import path
from . import views

app_name = 'salary'

urlpatterns = [
    path('status', views.SalaryStatus.as_view(), name="status"),
    path('status/daily', views.DailySalaryStatus.as_view(), name="daily_status"),
    path('status/weekly', views.WeeklySalaryStatus.as_view(), name="weekly_status"),
    path('table', views.SalaryTable.as_view(), name="table"),
    path('table2', views.SalaryTable2.as_view(), name="table2"),
    path('table3', views.SalaryTable3.as_view(), name="table3"),
    path('hourlywage/save', views.HourlyWageSaveView.as_view(), name="hourly_wage_save"),
    path('distribution', views.Salary_Distribution, name='distribution'),
    path('variation',views.Salary_Variation.as_view(), name='variation'),
    path('analysis',views.Salary_Analysis, name='Analysis'),
    path('test', views.test)
]