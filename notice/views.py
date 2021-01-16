from django.http import Http404, HttpResponse
from django.shortcuts import render, redirect
from django.views import generic
from .models import Notice, NoticeFile, NoticeComment
'''
class NoticeKindsView(generic.ListView):
    model = Notice
    template_name = 'notice/kinds.html'
    context_object_name = 'notices'

    #paginate_by = 2
    #한 페이지에 보여주는 객체 리스트의 갯수 지정
'''
def kinds(request, kinds):
    kinds_check(kinds)
    context = {
        'notices': Notice.objects.all(),
        'kinds':kinds,
    }
    return render(request, 'notice/kinds.html', context)

def create(request, kinds):
    return render(request, 'notice/create.html')

def detail(request, kinds, question_id):
    kinds_check(kinds)
    return render(request, 'notice/detail.html')

def delete(request, kinds, question_id):
    kinds_check(kinds)
    return redirect('/notice/{0}/'.format(kinds))

def kinds_check(kinds): # driver 나 office인지 체크
    if kinds != "driver" and kinds != "office":
        raise Http404