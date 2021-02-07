from django.urls import path
from . import views

app_name = 'dispatch'

urlpatterns = [
    #path('<str:kinds>/', views.NoticeKindsView.as_view(), name='kinds'),
    path('today/', views.TodayList.as_view(), name='today'),
    path('order/', views.OrderList.as_view(), name='order'),
    path('order/create/', views.order_create, name='order_create'),
    #path('order/create/', views.OrderCreate.as_view(), name='order_create'),
    path('order/<int:pk>/', views.OrderDetail.as_view(), name='order_detail'),
    #path('order/<int:pk>/edit/', views.order_edit, name='order_edit'),
    path('order/<int:pk>/edit/', views.OrderUpdate.as_view(), name='order_edit'),
    #path('order/<int:pk>/delete/', views.order_delete, name='order_delete'),
#
    #path('schedule/', views.ScheduleList.as_view(), name='schedule'),
    #path('schedule/<int:date>/', views.ScheduleDetail.as_view(), name='schedule_detail'),

    #path('management/', views.ManagementList.as_view(), name='management'),
    #path('management/<int:pk>/', views.ManagementDetail.as_view(), name='management_detail'),
    #path('management/<int:pk>/create/', views.management_create, name='management_create'),
    #path('management/<int:pk>/edit/', views.management_edit, name='management_edit'),
]