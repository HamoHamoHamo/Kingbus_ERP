from django.urls import path
from . import views

app_name = 'dispatch'

urlpatterns = [
    path('', views.DispatchList.as_view(), name='dispatch_list'),
    path('order/', views.OrderList.as_view(), name='order'),
    path('order/create/', views.order_create, name='order_create'),
    #path('order/create/', views.OrderCreate.as_view(), name='order_create'),
    path('order/<int:pk>/', views.OrderDetail.as_view(), name='order_detail'),
    path('order/<int:pk>/edit/', views.order_edit, name='order_edit'),
    #path('order/<int:pk>/edit/', views.OrderUpdate.as_view(), name='order_edit'),
    path('order/<int:pk>/delete/', views.order_delete, name='order_delete'),
    path('order/<int:pk>/management/create/', views.management_create, name='management_create'),
    path('order/<int:pk>/management/<int:c_pk>/edit/', views.management_edit, name='management_edit'),

    path('<str:date>/route/', views.DispatchDailyRouteList.as_view(), name='dispatch_daily_route'),
    path('<str:date>/bus/', views.DispatchDailyBusList.as_view(), name='dispatch_daily_bus'),
    
    path('schedule/', views.ScheduleList.as_view(), name='schedule'),
    path('schedule/<str:date>/', views.ScheduleDetail.as_view(), name='schedule_detail'),

    path('management/', views.ManagementList.as_view(), name='management'),
    #path('management/<int:pk>/', views.ManagementDetail.as_view(), name='management_detail'),
]