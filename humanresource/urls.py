from django.urls import path
from . import views

app_name = 'HR'

urlpatterns = [
    path('member', views.member, name='member'),
    path('mgmt', views.mgmt, name='mgmt'),

    # path('management/', views.ManagementList.as_view(), name='management'),
    # path('management/create/', views.HR_create, name='HR_create'),
    # path('management/delete/', views.HR_delete, name='HR_delete'),
    # path('management/<int:pk>/', views.HRDetail.as_view(), name='HR_detail'),
    # path('management/<int:pk>/edit/', views.HR_edit, name='HR_edit'),

    # path('member/', views.MemberList.as_view(), name='member'),
    # path('member/create/', views.member_create, name='member_create'),
    # path('member/delete/', views.member_delete, name='member_delete'),
    # path('member/<int:pk>/', views.MemberDetail.as_view(), name='member_detail'),
    # path('member/<int:pk>/<int:file_id>/', views.download, name='member_file_download'),
    # path('member/<int:pk>/<int:file_id>/del/', views.file_del, name='file_del'),
    # path('member/<int:pk>/edit/', views.member_edit, name='member_edit'),

]