from django.apps import AppConfig


class ApprovalConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'approval'

    def ready(self): # ready메소드 추가
    	import approval.signals
