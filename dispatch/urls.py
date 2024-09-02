from django.urls import path
from . import views

app_name = 'dispatch'

urlpatterns = [
    path('regularly', views.RegularlyDispatchList.as_view(), name="regularly"),
    path('regularly/create', views.regularly_connect_create, name="regularly_connect_create"),
    path('regularly/connect/load/<int:day>', views.regularly_connect_load, name="regularly_connect_load"),
    path('regularly/connect/delete', views.regularly_connect_delete, name="regularly_connect_delete"),
    path('regularly/route/time', views.RegularlyRouteTimeList.as_view(), name="regularly_route_time"),
    path('regularly/route', views.RegularlyRouteList.as_view(), name="regularly_route"),
    # path('regularly/fixed/create', views.regularly_fixed_create, name="regularly_fixed_create"),
    path('regularly/route/create', views.regularly_order_create, name="regularly_route_create"),
    path('regularly/route/edit', views.regularly_order_edit, name="regularly_route_edit"),
    path('regularly/route/upload', views.regularly_order_upload, name="regularly_route_upload"),
    path('regularly/route/download', views.regularly_order_download, name="regularly_route_download"),
    path('regularly/route/edit/check', views.regularly_order_edit_check, name="regularly_route_edit_check"),
    path('regularly/route/delete', views.regularly_order_delete, name="regularly_route_delete"),
    path('regularly/route/know', views.RegularlyRouteKnowList.as_view(), name="regularly_route_know"),
    path('regularly/route/know/create', views.regularly_route_know_create, name="regularly_route_know_create"),
    path('regularly/route/know/delete', views.regularly_route_know_delete, name="regularly_route_know_delete"),
    path('regularly/group/create', views.regularly_group_create, name="regularly_group_create"),
    path('regularly/group/edit', views.regularly_group_edit, name="regularly_group_edit"),
    path('regularly/group/delete', views.regularly_group_delete, name="regularly_group_delete"),
    path('regularly/group/fix', views.regularly_group_fix, name="regularly_group_fix"),
    path('regularly/connect', views.RegularlyConnectList.as_view(), name="regularly_connect"),
    path('regularly/business/edit', views.business_edit, name="business_edit"),

    
    # path('regularly/route/test', views.time_data, name="time_data"),
    
    path('regularly/station', views.RegularlyStationList.as_view(), name="regularly_station"),
    path('regularly/station/list', views.regularly_station_list, name="regularly_station_list"),
    path('regularly/station/create', views.regularly_station_create, name="regularly_station_create"),
    path('regularly/station/edit', views.regularly_station_edit, name="regularly_station_edit"),
    path('regularly/station/delete', views.regularly_station_delete, name="regularly_station_delete"),
    path('regularly/station/<int:id>', views.regularly_station, name="regularly_station"),
    path('regularly/station/upload', views.regularly_station_upload, name="regularly_station_upload"),
    path('regularly/station/download', views.regularly_station_download, name="regularly_station_download"),

    path('order', views.OrderList.as_view(), name="order"),
    path('order/create', views.order_connect_create, name="order_connect_create"),
    path('order/route/create', views.order_create, name="order_create"),
    path('order/route/edit', views.order_edit, name="order_edit"),
    path('order/route/edit/check', views.order_edit_check, name="order_edit_check"),
    path('order/route/delete', views.order_delete, name="order_delete"),
    path('order/route/upload', views.order_upload, name="order_upload"),
    path('order/route/download', views.order_download, name="order_download"),
    path('order/station', views.order_station_search, name="order_station_search"),
    path('order/tour/save', views.order_tour_save, name="order_tour_save"),
    path('order/tour/customer/save', views.order_tour_customer_save, name="order_tour_customer_save"),
    path('order/tour/customer/delete', views.order_tour_customer_delete, name="order_tour_customer_delete"),
    
    #운행확인
    path('schedule', views.ScheduleList.as_view(), name="schedule"),
    path('schedule2', views.ScheduleList2.as_view(), name="schedule2"),
    #배차거부
    path('refusal', views.RefusalList.as_view(), name="refusal"),
    path('refusal/delete', views.refusal_delete, name="refusal_delete"),
    # path('document', views.DocumentList.as_view(), name="document"),
    path('calendar/create', views.calendar_create, name='calendar_create'),
    # path('calendar/delete', views.calendar_delete, name='calendar_delete'),
    path('driving', views.DrivingList.as_view(), name='driving'),
    path('driving/history', views.driving_history, name='driving_history'),
    # 일정
    path('schedule/create', views.schedule_create, name='schedule_create'),
    path('schedule/delete', views.schedule_delete, name='schedule_delete'),
    # 배차지시서
    path('print/regularly', views.RegularlyPrintList.as_view(), name='regularly_print'),
    path('print/regularly/connect', views.RegularlyConnectPrintList.as_view(), name='regularly_connect_print'),
    path('print/order', views.order_print, name='order_print'),
    
    path('print/line', views.line_print, name='line_print'),
    path('print/bus', views.bus_print, name='bus_print'),
    path('print/dailylist', views.daily_driving_list, name='daily_driving_list'),
    path('print/daily', views.daily_driving_print, name='daily_driving_print'),
    path('print/estimate', views.print_estimate, name='estimate_print'),

]