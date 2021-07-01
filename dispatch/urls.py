from django.urls import path
from . import views

app_name = 'dispatch'

urlpatterns = [
    path('', views.DispatchList.as_view(), name='dispatch_list'),
    path('order/', views.OrderList.as_view(), name='order'),
    path('order/create/', views.order_create, name='order_create'),
    #path('order/<int:pk>/', views.OrderDetail.as_view(), name='order_detail'),
    path('order/<int:pk>/edit/', views.order_edit, name='order_edit'),
    path('order/<int:pk>/delete/', views.order_delete, name='order_delete'),
    
    #path('order/management/<int:pk>/create/', views.management_create, name='management_create'),
    #path('order/management/<int:pk>/<int:c_pk>/edit/', views.management_edit, name='management_edit'),
    #path('order/management/<int:pk>/<int:c_pk>/delete/', views.management_delete, name='management_delete'),

    path('regularly/', views.RegularlyOrderList.as_view(), name='regularly_order_list'),
    path('regularly/create/', views.regularly_order_create, name='regularly_order_create'),
    path('regularly/<int:pk>/edit/', views.regularly_order_edit, name='regularly_order_edit'),
    path('regularly/<int:pk>/delete/', views.regularly_order_delete, name='regularly_order_delete'),
    
    path('regularly/management/group/create/', views.regularly_order_group_create, name='regularly_order_group_create'),
    path('regularly/management/group/<int:pk>/edit/', views.regularly_order_group_edit, name='regularly_order_group_edit'),
    path('regularly/management/group/<int:pk>/delete/', views.regularly_order_group_delete, name='regularly_order_group_delete'),

    path('regularly/management/<int:pk>/create/', views.regularly_order_management_create, name='regularly_order_management_create'),
    path('regularly/management/<int:pk>/<int:c_pk>/edit/', views.regularly_order_management_edit, name='regularly_order_management_edit'),
    path('regularly/management/<int:pk>/<int:c_pk>/delete/', views.regularly_order_management_delete, name='regularly_order_management_delete'),


    path('<str:date>/route/', views.DispatchDailyRouteList.as_view(), name='dispatch_daily_route'),
    path('<str:date>/bus/', views.DispatchDailyBusList.as_view(), name='dispatch_daily_bus'),
    
    #path('schedule/', views.ScheduleList.as_view(), name='schedule'),
    path('schedule/<str:date>/', views.ScheduleDetail.as_view(), name='schedule_detail'),
]