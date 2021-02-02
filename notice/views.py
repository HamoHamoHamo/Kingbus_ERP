import urllib
import os
import mimetypes
from crudmember.models import User
from django.http import Http404, HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.views import generic
from notice.forms import NoticeForm
from notice.models import Notice, NoticeFile, NoticeComment, NoticeViewCnt
from ERP.settings import BASE_DIR
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
        notice_file_save(files, notice)
        #auth.login(request, user)
        return redirect(reverse('notice:detail', args=(kinds,notice.id)))
    return render(request, 'notice/create.html')

def notice_file_save(upload_file, notice):
    for file in upload_file:
        notice_file = NoticeFile(
            notice_id=notice,
            file=file,
            filename=file.name,
        )
        notice_file.save()
    return

def edit(request, kinds, notice_id):
    notice = get_object_or_404(Notice, pk=notice_id)

    if request.method == "GET":
        context = {
            'notice':notice,
            'notice_files':NoticeFile.objects.filter(notice_id=notice_id),
        }
        return render(request, "notice/edit.html", context )
    else:
        upload_file = request.FILES.getlist('file', None)

        notice.title=request.POST.get('title', None)
        notice.content=request.POST.get('content', None)
        notice.kinds=request.POST.get('kinds', None)
        notice.save()

        notice_file_save(upload_file, notice)
    return redirect('/notice/{0}/{1}'.format(kinds, notice_id))

### genericview update 테스트
'''
class NoticeEdit(generic.UpdateView):
    model = Notice
    context_object_name = 'notice'
    template_name = 'notice/edit.html' 
    success_url = '/'

    #get object
    def get_object(self): 
        notice = get_object_or_404(Notice, pk=self.kwargs['pk']) 

        return notice
'''
####################### 테스트        
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

def download(request, kinds, notice_id, file_id):
    kinds_check(kinds)
    download_file = get_object_or_404(NoticeFile, pk=file_id)
    url = download_file.file.url
    root = str(BASE_DIR)+url
    print("\n테스트\n", root)

    if os.path.exists(root):
        with open(root, 'rb') as fh:
            quote_file_url = urllib.parse.quote(download_file.filename.encode('utf-8'))
            response = HttpResponse(fh.read(), content_type=mimetypes.guess_type(url)[0])
            response['Content-Disposition'] = 'attachment;filename*=UTF-8\'\'%s' % quote_file_url
            return response
        raise Http404
    else:
        print("에러")
        raise Http404

def delete(request, kinds, notice_id):
    kinds_check(kinds)
    notice = Notice.objects.get(pk=notice_id)
    notice_file = notice.file.all()
    if creator_check(request, notice_id, Notice):
        if notice_file:
            for file in notice_file:
                os.remove(file.file.path)
        notice.delete()
    return redirect('/notice/{0}/'.format(kinds))

def file_del(request, kinds, notice_id, file_id):
    kinds_check(kinds)
    notice = Notice.objects.get(pk=notice_id)
    file = NoticeFile.objects.get(pk=file_id)
    os.remove(file.file.path)
    file.delete()
    
    context = {
        'notice':notice,
        'notice_files':NoticeFile.objects.filter(notice_id=notice_id),
    }
    return render(request, "notice/edit.html", context )

def comment_del(request, kinds, notice_id, comment_id):
    kinds_check(kinds)
    if creator_check(request, comment_id, NoticeComment):
        NoticeComment.objects.filter(id=comment_id).delete()
    return redirect('/notice/{0}/{1}'.format(kinds, notice_id))

def creator_check(request, pk, type):
    if request.session['user'] != type.objects.get(id=pk).creator.id:
        raise Http404
    return True

def kinds_check(kinds): # driver 나 office인지 체크
    if kinds != "driver" and kinds != "office":
        raise Http404
    return True

