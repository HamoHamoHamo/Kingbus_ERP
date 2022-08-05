from django.apps import AppConfig


class DispatchConfig(AppConfig):
    name = 'dispatch'

    def ready(self): # ready메소드 추가
    	import dispatch.signals
