from django.urls import path
from . import views

app_name = 'dispatch'

urlpatterns = [
    path('regularly', views.RegularlyDispatchList.as_view(), name="regularly"),
    path('regularly/create', views.regularly_connect_create, name="regularly_connect_create"),
    path('regularly/connect/load/<int:week>', views.regularly_connect_load, name="regularly_connect_load"),
    path('regularly/connect/delete', views.regularly_connect_delete, name="regularly_connect_delete"),
    path('regularly/route', views.RegularlyRouteList.as_view(), name="regularly_route"),
    # path('regularly/fixed/create', views.regularly_fixed_create, name="regularly_fixed_create"),
    path('regularly/route/create', views.regularly_order_create, name="regularly_route_create"),
    path('regularly/route/edit', views.regularly_order_edit, name="regularly_route_edit"),
    path('regularly/route/upload', views.regularly_order_upload, name="regularly_route_upload"),
    # path('regularly/route/edit/check', views.regularly_order_edit_check, name="regularly_route_edit_check"),
    path('regularly/route/delete', views.regularly_order_delete, name="regularly_route_delete"),
    path('regularly/group/create', views.regularly_group_create, name="regularly_group_create"),
    path('regularly/group/edit', views.regularly_group_edit, name="regularly_group_edit"),
    path('regularly/group/delete', views.regularly_group_delete, name="regularly_group_delete"),
    path('regularly/group/fix', views.regularly_group_fix, name="regularly_group_fix"),

    path('order', views.OrderList.as_view(), name="order"),
    path('order/create', views.order_connect_create, name="order_connect_create"),
    path('order/route/create', views.order_create, name="order_create"),
    path('order/route/edit', views.order_edit, name="order_edit"),
    path('order/route/edit/check', views.order_edit_check, name="order_edit_check"),
    path('order/route/delete', views.order_delete, name="order_delete"),
    path('schedule', views.ScheduleList.as_view(), name="schedule"),
    # path('document', views.DocumentList.as_view(), name="document"),
    # 일정
    path('calendar/create', views.calendar_create, name='calendar_create'),
    path('calendar/delete/1', views.calendar_delete_1, name='calendar_delete1'),
    path('schedule/create', views.schedule_create, name='schedule_create'),
    path('schedule/delete', views.schedule_delete, name='schedule_delete'),
    # 배차지시서
    path('print/regularly', views.RegularlyPrintList.as_view(), name='regularly_print'),
    path('print/order', views.order_print, name='order_print'),
    path('print/line', views.line_print, name='line_print'),
    path('print/bus', views.bus_print, name='bus_print'),
    path('print/dailylist', views.daily_driving_list, name='daily_driving_list'),
    path('print/daily', views.daily_driving_print, name='daily_driving_print'),
]