from django.urls import path
from . import views

app_name = 'salary'

urlpatterns = [
    path('status', views.SalaryStatus.as_view(), name="status"),
    path('status/daily', views.DailySalaryStatus.as_view(), name="daily_status"),
    path('table', views.SalaryTable.as_view(), name="table"),
    path('table2', views.SalaryTable2.as_view(), name="table2"),
    path('hourlywage/save', views.HourlyWageSaveView.as_view(), name="hourly_wage_save"),
    path('daily_status', views.DailyStatusView.as_view(), name='daily_status'),
    path('weekly_status', views.WeeklyStatusView.as_view(), name='weekly_status'),
    path('weekly_statustwo', views.WeeklyStatusTwoView.as_view(), name='weekly_statustwo'),
    path('Salary_Distribution2', views.SalaryDistribution2.as_view(), name='Salary_Distribution2'),
    path('salary_change', views.SalaryChange.as_view(), name='salary_change'),
    path('gptgraph', views.GptGraph.as_view(), name='gptgraph'),
    path('routeTime', views.RouteTime.as_view(), name='routeTime'),
]
