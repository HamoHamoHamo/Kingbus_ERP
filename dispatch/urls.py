from django.urls import path
from . import views

app_name = 'dispatch'

urlpatterns = [
    #path('<str:kinds>/', views.NoticeKindsView.as_view(), name='kinds'),
    path('', views.home, name='home'),
    path('order/', views.order, name='order'),
    path('order/<int:pk>/', views.DispatchOrderDetail.as_view(), name='detail'),
    path('order/<int:pk>/delete/', views.order_delete, name='order_delete'),
    path('order/<int:pk>/create/', views.order_create, name='order_create'),
    path('order/<int:pk>/edit/', views.order_edit, name='order_edit'),

    path('direction/', views.direction, name='direction'),

    path('management/', views.management, name='management'),
    path('management/<int:order_id>', views.management, name='management'),


    path('<str:kinds>/', views.kinds, name='kinds'),
    path('<str:kinds>/<int:pk>/', views.NoticeDetail.as_view(), name='detail'),
    path('<str:kinds>/<int:notice_id>/<int:file_id>/', views.download, name='download'),
    path('<str:kinds>/<int:notice_id>/edit/', views.edit, name='edit'),

    path('<str:kinds>/<int:notice_id>/delete/', views.delete, name='delete'),
    path('<str:kinds>/<int:notice_id>/<int:file_id>/file-del/', views.file_del, name='file_del'),
    path('<str:kinds>/<int:notice_id>/<int:comment_id>/delete/', views.comment_del, name='comment_del'),
]