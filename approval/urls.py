from django.urls import path
from . import views

appname= 'approval'

urlpatterns = [
    path('approval', views.Approval.as_view(), name='approval'),
    path('approval_process', views.ApprovalProcess.as_view(), name='approval_process'),
]