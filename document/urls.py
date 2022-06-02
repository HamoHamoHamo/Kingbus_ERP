from django.urls import path
from . import views

app_name = 'document'

urlpatterns = [
    path('', views.DocumentList.as_view(), name='document_list'),
    path('create/', views.document_create, name='document_create'),
    path('<int:pk>/', views.DocumentDetail.as_view(), name='document_detail'),
    path('<int:pk>/edit/', views.document_edit, name='document_edit'),
    path('<int:pk>/delete/', views.document_delete, name='document_delete'),
    path('<int:pk>/<int:file_id>/', views.download, name='document_download'),
    path('<int:pk>/<int:file_id>/delete', views.file_delete, name='file_delete'),
]