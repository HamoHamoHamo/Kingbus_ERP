from django.shortcuts import redirect
from django.conf import settings
from django.db import connection
from django.template import Template, Context
from ipware.ip import get_client_ip
from crudmember.models import UserIP

class LoginCheckMiddleware(object):
    def __init__(self, get_response):
        self.get_response = get_response
        self.check_url = [
            "/notice",
            "/accounting",
            "/dispatch",
            "/HR",
            "/vehicle",
        ]
        # One-time configuration and initialization.
    def __call__(self, request):
        # Code to be executed for each request before
        # the view (and later middleware) are called.
        response = self.get_response(request)
        
        
        # ip 확인
        ip = get_client_ip(request)
        ip=ip[0]
        if ip:
            if ip != "59.29.60.206" and ip != '115.40.25.236':
                print(ip)

            try:
                UserIP.objects.get(ip=ip)
            except Exception as error:
                print("\nip저장", error)
                userip=UserIP(ip=ip)
                userip.save()
            
            

        else:
            print ("못찾았다")

            
        
        # 로그인 되어 있지 않은 상태로 check_url에 접속시 로그인 화면으로 이동
        if not 'user' in request.session:
            for i in self.check_url:
                if request.path_info.startswith(i):
                    return redirect("crudmember:login")
            #return redirect('crudmember:login')
        # Code to be executed for each request/response after
        # the view is called.

        return response