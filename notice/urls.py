from django.urls import path
from . import views

app_name = 'notice'

urlpatterns = [
    #path('<str:kinds>/', views.NoticeKindsView.as_view(), name='kinds'),
    path('create', views.create, name='create'),
    path('<str:kinds>', views.NoticeKindsView.as_view(), name='kinds'),
    path('<str:kinds>/<int:pk>', views.NoticeDetail.as_view(), name='detail'),
    path('<str:kinds>/<int:notice_id>/<int:file_id>', views.download, name='download'),
    path('<str:kinds>/<int:notice_id>/edit', views.edit, name='edit'),
    #path('<str:kinds>/<int:pk>/edit', views.NoticeEdit.as_view(), name='edit'),

    path('<str:kinds>/<int:notice_id>/delete', views.delete, name='delete'),
    path('<str:kinds>/<int:notice_id>/<int:file_id>/file-del', views.file_del, name='file_del'),
    path('<str:kinds>/<int:notice_id>/<int:comment_id>/delete', views.comment_del, name='comment_del'),

    # 수칙
    path('rule/approval', views.approval_rule, name='approval_rule'),
    path('rule/rollcall', views.roll_call_rule, name='roll_call_rule'),
    path('rule/driver', views.driver_rule, name='driver_rule'),
    path('rule/manager', views.manager_rule, name='manager_rule'),
    path('rule/fieldmanager', views.field_manager_rule, name='field_manager_rule'),
    path('rule/personnelcommittee', views.personnel_committee_rule, name='personnel_committee_rule'),

    path('rule/approval/print', views.approval_rule_print, name='approval_rule_print'),
    path('rule/rollcall/print', views.roll_call_rule_print, name='roll_call_rule_print'),
    path('rule/driver/print', views.driver_rule_print, name='driver_rule_print'),
    path('rule/manager/print', views.manager_rule_print, name='manager_rule_print'),
    path('rule/fieldmanager/print', views.field_manager_rule_print, name='field_manager_rule_print'),
    path('rule/personnelcommittee/print', views.personnel_committee_rule_print, name='personnel_committee_rule_print'),
    
    path('rule/organizationchart', views.organizationchart, name='organizationchart'),
]