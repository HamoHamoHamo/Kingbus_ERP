from django.urls import path
from . import views

app_name = 'dispatch'

urlpatterns = [
    #path('<str:kinds>/', views.NoticeKindsView.as_view(), name='kinds'),
    path('', views.home, name='home'),
    path('order/', views.order, name='order'),
    path('order/create/', views.order_create, name='order_create'),
    path('order/<int:order_id>/', views.order_detail, name='order_detail'),
    path('order/<int:order_id>/delete/', views.order_delete, name='order_delete'),
    path('order/<int:order_id>/edit/', views.order_edit, name='order_edit'),

    path('schedule/', views.schedule, name='schedule'),

    path('management/', views.management, name='management'),
    path('management/<int:order_id>/', views.management_detail, name='management_detail'),
    path('management/<int:order_id>/create/', views.management_create, name='management_create'),
    path('management/<int:order_id>/edit/', views.management_edit, name='management_edit'),
]