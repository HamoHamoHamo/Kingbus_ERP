from django.http import Http404, HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.views import generic
from .models import Notice, NoticeFile, NoticeComment
from crudmember.models import User
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
        'notices': Notice.objects.all().filter(kinds=kinds).order_by('-pub_date')[:10],
        'kinds':kinds,
    }
    return render(request, 'notice/kinds.html', context)

def create(request):
    if request.method == "GET":
        return render(request, 'notice/create.html')

    elif request.method == 'POST':
        title = request.POST.get('title', None)
        content = request.POST.get('content', None)
        kinds = request.POST.get('kinds', None)
        files = request.FILES.getlist('file', None)
        
        user_id = request.session['user']
        user = User.objects.get(pk=user_id)
        
        notice = Notice(
            creator = user,
            title = title,
            content = content,
            kinds = kinds
            )
        notice.save()
        print("테스트", type(notice))
        for upload_file in files:
            notice_file = NoticeFile(
                notice_id=notice,
                file=upload_file
            )
            notice_file.save()
        #auth.login(request, user)
        return redirect('notice:detail', args=(kinds,notice))
    return render(request, 'notice/create.html')


class NoticeDetailList(generic.DetailView):
    template_name = 'notice/detail.html'
    context_object_name = 'notice'
    
    def post(self, request, *args, **kwargs):
        user_id = request.session['user']
        user = User.objects.get(pk=user_id)
        content = request.POST.get('content', None)
        self.notice_id=self.kwargs['pk']
        notice = Notice.objects.get(id=self.notice_id)
        print("테스트",notice)
        notice_comment = NoticeComment(
            creator = user,
            notice_id = notice,
            content = content,
        )
        notice_comment.save()
        return redirect('notice:detail', args=(self.kwargs['kinds'],self.notice_id))


    def get_queryset(self):
        self.notice_id=self.kwargs['pk']
        self.notice = get_object_or_404(Notice, id=self.notice_id)
        print("테스트", self.notice, type(self.notice))
        return Notice.objects.filter(title=self.notice)

    def get_context_data(self, **kwargs):
        # 기본 구현을 호출해 context를 가져온다.
        context = super(NoticeDetailList, self).get_context_data(**kwargs)
        # 모든 책을 쿼리한 집합을 context 객체에 추가한다.
        context['notice'] = self.notice
        context['notice_files'] = NoticeFile.objects.filter(notice_id=self.notice_id)
        context['notice_comments'] = NoticeComment.objects.filter(notice_id=self.notice_id)
        return context
    #paginate_by = 2
    #한 페이지에 보여주는 객체 리스트의 갯수 지정


def detail(request, kinds, question_id):
    kinds_check(kinds)

    return render(request, 'notice/detail.html')

def delete(request, kinds, question_id):
    kinds_check(kinds)
    return redirect('/notice/{0}/'.format(kinds))

def kinds_check(kinds): # driver 나 office인지 체크
    if kinds != "driver" and kinds != "office":
        raise Http404