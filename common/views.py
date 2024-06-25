from django.shortcuts import render, redirect
from django.views import View
from django.http import HttpResponse
from humanresource.models import Member

class AuthorityCheckView(View):
    authority_level = 3
    

    def dispatch(self, request, *args, **kwargs):
        # 여기에서 요청을 처리하기 전에 공통적인 작업을 수행합니다.
        if request.session.get('authority') > self.authority_level:
            return render(request, 'authority.html')
        
        self.creator = Member.objects.get(pk=request.session['user'])
        # 요청을 처리하기 위해 부모 클래스의 dispatch 메소드를 호출합니다.
        return super().dispatch(request, *args, **kwargs)
