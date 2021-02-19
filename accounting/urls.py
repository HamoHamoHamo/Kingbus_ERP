from django.urls import path
from . import views

app_name = 'accounting'

urlpatterns = [
    path('outlay/', views.OutlayList.as_view(), name='outlay'),
    path('outlay/create', views.outlay_create, name='outlay_create'),
    path('outlay/<int:pk>', views.outlay_detail, name='outlay_detail'),
    path('outlay/<int:pk>/delete', views.outlay_detail, name='outlay_detail'),
    path('outlay/<int:pk>/edit', views.outlay_detail, name='outlay_detail'),
    
]
