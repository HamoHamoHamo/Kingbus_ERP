from django.db.models import Q

from .models import Member

class MemberSelector:
    def get_using_driver_list(self, name):
        member = Member.objects.filter(use='사용').filter(Q(role='팀장')|Q(role='운전원')|Q(role='용역')|Q(role='임시')).order_by('name')
        if name:
            member = member.filter(name__startswith=name)
        return member