from django.urls import path
from . import views

app_name = 'HR'

urlpatterns = [
    path('management/', views.ManagementList.as_view(), name='management'),
    path('management/create/', views.HR_create, name='HR_create'),
    path('management/<int:pk>/edit/', views.HR_edit, name='HR_edit'),
    path('management/<int:pk>/delete/', views.HR_delete, name='HR_delete'),

    path('member/create/', views.member_create, name='member_create'),
    path('member/<int:pk>/', views.MemberDetail.as_view(), name='member_detail'),
    path('member/<int:pk>/edit', views.member_edit, name='member_edit'),
    path('member/<int:pk>/delete', views.member_delete, name='member_delete'),

]