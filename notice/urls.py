from django.urls import path
from . import views

app_name = 'notice'

urlpatterns = [
    #path('<str:kinds>/', views.NoticeKindsView.as_view(), name='kinds'),
    path('create/', views.create, name='create'),
    path('<str:kinds>/', views.kinds, name='kinds'),
    path('<str:kinds>/<int:question_id>/', views.detail, name='detail'),
    path('<str:kinds>/<int:question_id>/delete/', views.delete, name='delete'),
]