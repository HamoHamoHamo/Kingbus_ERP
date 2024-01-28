from django.apps import AppConfig


class HumanresourceConfig(AppConfig):
    name = 'humanresource'

    def ready(self): # ready메소드 추가
    	import humanresource.signals
