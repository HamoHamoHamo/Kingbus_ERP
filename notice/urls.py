from django.urls import path
from . import views

app_name = 'notice'

urlpatterns = [
    #path('<str:kinds>/', views.NoticeKindsView.as_view(), name='kinds'),
    path('create/', views.create, name='create'),
    path('<str:kinds>/', views.kinds, name='kinds'),
    path('<str:kinds>/<int:pk>/', views.NoticeDetail.as_view(), name='detail'),
    path('<str:kinds>/<int:notice_id>/<int:file_id>/', views.download, name='download'),
    path('<str:kinds>/<int:notice_id>/edit/', views.edit, name='edit'),
    #path('<str:kinds>/<int:pk>/edit/', views.NoticeEdit.as_view(), name='edit'),

    path('<str:kinds>/<int:notice_id>/delete/', views.delete, name='delete'),
    path('<str:kinds>/<int:notice_id>/<int:file_id>/file-del/', views.file_del, name='file_del'),
    path('<str:kinds>/<int:notice_id>/<int:comment_id>/delete/', views.comment_del, name='comment_del'),
]