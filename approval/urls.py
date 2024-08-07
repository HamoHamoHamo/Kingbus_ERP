from django.urls import path
from . import views

appname= 'approval'

urlpatterns = [
    path('approvalwrite/', views.ApprovalWrite.as_view(), name='approvalwrite'),
    path('approvaldisposal/', views.ApprovalDisposal.as_view(), name='approvaldisposal'),
]