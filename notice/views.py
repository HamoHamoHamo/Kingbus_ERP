import urllib, os, mimetypes
from crudmember.models import User
from django.http import Http404, HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.views import generic
from .models import Notice, NoticeFile, NoticeComment, NoticeViewCnt
'''
class NoticeKindsView(generic.ListView):
    model = Notice
    template_name = 'notice/kinds.html'
    context_object_name = 'notices'

    #paginate_by = 2
    #한 페이지에 보여주는 객체 리스트의 갯수 지정
'''
def home(request):
    return render(request, 'notice/home.html')

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
        for upload_file in files:
            notice_file = NoticeFile(
                notice_id=notice,
                file=upload_file,
                filename=upload_file.name,
            )
            notice_file.save()
        #auth.login(request, user)
        return redirect(reverse('notice:detail', args=(kinds,notice.id)))
    return render(request, 'notice/create.html')

# detail
class NoticeDetail(generic.DetailView):
    template_name = 'notice/detail.html'
    context_object_name = 'notice'
    
    def post(self, request, *args, **kwargs):
        self.user_id = request.session['user']
        user = User.objects.get(pk=self.user_id)
        content = request.POST.get('content', None)
        self.notice_id=self.kwargs['pk']
        notice = Notice.objects.get(id=self.notice_id)
        print("테스트",type(self.notice_id))
        notice_comment = NoticeComment(
            creator = user,
            notice_id = notice,
            content = content,
        )
        notice_comment.save()
        return redirect(reverse('notice:detail', args=(self.kwargs['kinds'], self.notice_id)))


    def get_queryset(self):
        self.user_id = self.request.session['user']
        self.user = User.objects.get(pk=self.user_id)
        self.notice_id=self.kwargs['pk']
        self.notice = get_object_or_404(Notice, id=self.notice_id)
        return Notice.objects.filter(title=self.notice)

    def get_context_data(self, **kwargs):
        # 기본 구현을 호출해 context를 가져온다.
        context = super(NoticeDetail, self).get_context_data(**kwargs)
        context['logged_user'] = self.request.session['user']
        context['view_cnt'] = self.get_view_cnt()
        context['notice'] = self.notice
        context['notice_files'] = NoticeFile.objects.filter(notice_id=self.notice_id)
        context['notice_comments'] = NoticeComment.objects.filter(notice_id=self.notice_id)
        return context
    #paginate_by = 2
    #한 페이지에 보여주는 객체 리스트의 갯수 지정

    def get_view_cnt(self):
        try:
            view_cnt = NoticeViewCnt.objects.get(
                user_id=self.user,
                notice_id=self.notice
                )
        except Exception as e:
            # 처음 게시글을 조회한 경우엔 조회 기록이 없음
            print("error:", e)
            view_cnt = NoticeViewCnt(
                user_id=self.user,
                notice_id=self.notice
                )
            view_cnt.save()
        
        cnt = NoticeViewCnt.objects.filter(notice_id=self.notice_id).count()
        return cnt



def detail(request, kinds, notice_id):
    kinds_check(kinds)
    return render(request, 'notice/detail.html')

def delete(request, kinds, notice_id):
    kinds_check(kinds)
    if notice_creator_check(request, notice_id):
        Notice.objects.filter(id=notice_id).delete()
    return redirect('/notice/{0}/'.format(kinds))

def download(request, kinds, notice_id, file_id):
    kinds_check(kinds)
    download_file = get_object_or_404(NoticeFile, pk=file_id)
    url = download_file.file.url
    file_url = urllib.parse.unquote(url)
    if os.path.exists(file_url):
        with open(file_url, 'rb') as fh:
            quote_file_url = urllib.parse.quote(notice.filename.encode('utf-8'))
            response = HttpResponse(fh.read(), content_type=mimetypes.guess_type(file_url)[0])
            response['Content-Disposition'] = 'attachment;filename*=UTF-8\'\'%s' % quote_file_url
            return response
        raise Http404

def comment_del(request, kinds, notice_id, comment_id):
    kinds_check(kinds)
    if comment_creator_check(request, comment_id):
        NoticeComment.objects.filter(id=comment_id).delete()
    return redirect('/notice/{0}/{1}'.format(kinds, notice_id))

def notice_creator_check(request, notice_id):
    if request.session['user'] != Notice.objects.get(id=notice_id).creator:
        raise Http404
    return True

def comment_creator_check(request, comment_id):
    if request.session['user'] != NoticeComment.objects.get(id=comment_id).creator:
        raise Http404
    return True

def kinds_check(kinds): # driver 나 office인지 체크
    if kinds != "driver" and kinds != "office":
        raise Http404
    return True