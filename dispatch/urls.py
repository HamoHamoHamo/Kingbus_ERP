from django.urls import path
from . import views

app_name = 'dispatch'

urlpatterns = [
    path('regularly', views.RegularlyDispatchList.as_view(), name="regularly"),
    path('regularly/create', views.regularly_connect_create, name="regularly_connect_create"),
    path('regularly/route', views.RegularlyRouteList.as_view(), name="regularly_route"),
    path('regularly/route/create', views.regularly_order_create, name="regularly_route_create"),
    path('regularly/route/edit', views.regularly_order_edit, name="regularly_route_edit"),
    path('regularly/route/delete', views.regularly_order_delete, name="regularly_route_delete"),
    path('regularly/group/create', views.regularly_group_create, name="regularly_group_create"),
    path('regularly/group/edit', views.regularly_group_edit, name="regularly_group_edit"),
    path('regularly/group/delete', views.regularly_group_delete, name="regularly_group_delete"),
    path('order', views.OrderList.as_view(), name="order"),
    path('order/create', views.order_connect_create, name="order_connect_create"),
    path('order/route/create', views.order_create, name="order_create"),
    path('order/route/edit', views.order_edit, name="order_edit"),
    path('order/route/delete', views.order_delete, name="order_delete"),
    path('schedule', views.schedule, name="schedule"),
    path('document', views.DocumentList.as_view(), name="document"),

    # path('', views.DispatchList.as_view(), name='dispatch_list'),
    # path('order/', views.OrderList.as_view(), name='order'),
    # path('order/create/', views.order_create, name='order_create'),
    # path('order/<int:pk>/', views.OrderDetail.as_view(), name='order_detail'),
    # path('order/<int:pk>/edit/', views.order_edit, name='order_edit'),
    # path('order/delete/', views.order_delete, name='order_delete'),
    
    # path('regularly/', views.RegularlyOrderList.as_view(), name='regularly'),
    # path('regularly/create/', views.regularly_order_create, name='regularly_order_create'),
    # path('regularly/<int:pk>/', views.RegularlyOrderDetail.as_view(), name='regularly_order_detail'),
    # path('regularly/<int:pk>/edit/', views.regularly_order_edit, name='regularly_order_edit'),
    # path('regularly/order/delete/', views.regularly_order_delete, name='regularly_order_delete'),
    
    # path('regularly/group/', views.RegularlyOrderGroup.as_view(), name='regularly_order_group'),
    # path('regularly/group/create/', views.regularly_group_create, name='regularly_group_create'),
    # path('regularly/group/delete/', views.regularly_group_delete, name='regularly_group_delete'),
    # path('regularly/group/<int:pk>/', views.RegularlyOrderGroupDetail.as_view(), name='regularly_order_group_detail'),
    # path('regularly/group/<int:pk>/create/', views.regularly_order_group_create, name='regularly_order_group_create'),
    # path('regularly/group/<int:pk>/delete/', views.regularly_order_group_delete, name='regularly_order_group_delete'),
        #path('regularly/group/<int:pk>/edit/', views.regularly_order_group_edit, name='regularly_order_group_edit'),

        #path('regularly/management/', views.RegularlyOrderManagement.as_view(), name='regularly_order_management'),
        #path('regularly/management/<int:pk>/<int:c_pk>/edit/', views.regularly_order_management_edit, name='regularly_order_management_edit'),
        #path('regularly/management/<int:pk>/<int:c_pk>/delete/', views.regularly_order_management_delete, name='regularly_order_management_delete'),

    # path('mgt/', views.Management.as_view(), name='mgt'),
    # path('mgt/create/', views.management_create, name='mgt_create'),    
    # path('mgt/<int:pk>/', views.ManagementDetail.as_view(), name='mgt_detail'),
        #path('mgt/<int:pk>/r/', views.ManagementDetailR.as_view(), name='mgt_detail_r'),
        #path('mgt/<int:pk>/delete/', views.mgt_delete, name='mgt_delete'),
        
        #path('schedule/<str:date>/', views.ScheduleDetail.as_view(), name='schedule_detail'),

    # path('<str:date>/route/', views.DispatchDailyRouteList.as_view(), name='dispatch_daily_route'),
    # path('<str:date>/bus/', views.DispatchDailyBusList.as_view(), name='dispatch_daily_bus'),
    
    #path('schedule/', views.ScheduleList.as_view(), name='schedule'),
]