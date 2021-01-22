from django.urls import path
from . import views

app_name = 'notice'

urlpatterns = [
    #path('<str:kinds>/', views.NoticeKindsView.as_view(), name='kinds'),
    path('', views.home, name='home'),
    path('create/', views.create, name='create'),
    path('<str:kinds>/', views.kinds, name='kinds'),
    path('<str:kinds>/<int:pk>/', views.NoticeDetail.as_view(), name='detail'),
    path('<str:kinds>/<int:notice_id>/delete/', views.delete, name='delete'),
    path('<str:kinds>/<int:notice_id>/<int:comment_id>/delete/', views.comment_del, name='comment_del'),
]