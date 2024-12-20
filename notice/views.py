import urllib
import os
import mimetypes
from django.http import Http404, HttpResponse, HttpResponseNotAllowed
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.views import generic
from humanresource.models import Member
from humanresource.views import send_message
from notice.forms import NoticeForm
from notice.models import Notice, NoticeFile, NoticeComment, NoticeViewCnt
from config.settings.base import BASE_DIR
'''
class NoticeKindsView(generic.ListView):
    model = Notice
    template_name = 'notice/kinds.html'
    context_object_name = 'notices'

    #paginate_by = 2
    #한 페이지에 보여주는 객체 리스트의 갯수 지정

'''

class NoticeKindsView(generic.ListView):
    template_name = 'notice/kinds.html'
    context_object_name = 'notices'
    paginate_by = 10
    model = Notice

    def search_result(self, request, kinds):
        if request.GET.get('search', None):
            selector = request.GET.get('top_box_selector', None)
            search = request.GET.get('search', '')
            if selector == 'title':
                notices = Notice.objects.filter(title__contains=search).filter(kinds=kinds).order_by('-pub_date')
            elif selector == "creator":                
                notices = Notice.objects.filter(creator__name__contains=search).filter(kinds=kinds).order_by('-pub_date')
                

            else:
                raise Http404()
            return notices
        else:
            return None
    
    def get(self, request, **kwargs):
        if request.session.get('authority') >= 3 and self.kwargs['kinds'] == 'office':
            return render(request, 'authority.html')
        else:
            return super().get(request, **kwargs)

    def get_queryset(self):
        notices = self.search_result(self.request, self.kwargs['kinds'])
        if notices is None:
            kinds_check(self.kwargs['kinds'])
            notices = Notice.objects.all().filter(kinds=self.kwargs['kinds']).order_by('-pub_date')
        return notices

    # 페이징 처리
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        paginator = context['paginator']
        page_numbers_range = 5
        max_index = len(paginator.page_range)
        page = self.request.GET.get('page')
        current_page = int(page) if page else 1

        start_index = int((current_page - 1) / page_numbers_range) * page_numbers_range
        end_index = start_index + page_numbers_range
        if end_index >= max_index:
            end_index = max_index
        page_range = paginator.page_range[start_index:end_index]
        context['page_range'] = page_range
        context['current_page'] = current_page

        context['start_num'] = paginator.count - paginator.per_page * (current_page-1)
        
        context['kinds'] = self.kwargs['kinds']
        
        context['search'] = self.request.GET.get('search', '')
        context['selector'] = self.request.GET.get('top_box_selector', 'title')
        return context

def create(request):
    context={
        'name': get_object_or_404(Member, pk=request.session.get('user')).name,
        'kinds': request.GET.get('kinds')
        }
    if request.session.get('authority') >= 3:
        return render(request, 'authority.html')
    if request.method == "GET":
        
        return render(request, 'notice/create.html', context)

    elif request.method == 'POST':
        creator = get_object_or_404(Member, pk=request.session.get('user'))
        notice_form = NoticeForm(request.POST)
        
        files = request.FILES.getlist('file', None)
        if notice_form.is_valid():
            notice = notice_form.save(commit=False)
            notice.creator = creator
            notice.save()
            notice_file_save(files, notice)
        #auth.login(request, user)
        if notice.kinds == 'driver':
            send_message('공지를 확인해 주세요', notice.title, None, 'trp')

        return redirect(reverse('notice:kinds', args=(notice.kinds,)))
    return render(request, 'notice/create.html', context)

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
    if Notice.objects.get(id=notice_id).creator.id != request.session.get('user'):
        return render(request, 'authority.html')
    notice = get_object_or_404(Notice, pk=notice_id)

    if request.method == "GET":
        context = {
            'notice':notice,
            'notice_files':NoticeFile.objects.filter(notice_id=notice_id),
        }
        
        return render(request, "notice/edit.html", context )
    else:
        notice_form = NoticeForm(request.POST)
        files = request.FILES.getlist('file', None)
        if notice_form.is_valid() and notice.creator.id == request.session['user']:
            notice.title=notice_form.cleaned_data['title']
            notice.content=notice_form.cleaned_data['content']
            notice.kinds=notice_form.cleaned_data['kinds']
            notice.save()
            notice_file_save(files, notice)
        else:
            raise Http404
    return redirect('/notice/{0}/{1}'.format(kinds, notice_id))

# detail
class NoticeDetail(generic.DetailView):
    template_name = 'notice/detail.html'
    context_object_name = 'notice'
    model = Notice
    
    def post(self, request, *args, **kwargs):
        self.user_id = request.session.get('user')
        user = Member.objects.get(pk=self.user_id)
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

    def get(self, request, **kwargs):
        if request.session.get('authority') >= 3 and self.kwargs['kinds'] == 'office':
            return render(request, 'authority.html')
        else:
            return super().get(request, **kwargs)
            
    def get_queryset(self):
        self.user = Member.objects.get(pk=self.request.session.get('user'))
        self.notice_id=self.kwargs['pk']
        self.notice = get_object_or_404(Notice, id=self.notice_id)
        return Notice.objects.filter(title=self.notice)

    def get_context_data(self, **kwargs):
        # 기본 구현을 호출해 context를 가져온다.
        context = super(NoticeDetail, self).get_context_data(**kwargs)
        
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
            view_cnt = NoticeViewCnt(
                user_id=self.user,
                notice_id=self.notice
                )
            view_cnt.save()

        cnt = NoticeViewCnt.objects.filter(notice_id=self.notice_id).count()
        notice = Notice.objects.get(pk=self.notice_id)
        notice.view_cnt = cnt
        notice.save()
        return cnt

def download(request, kinds, notice_id, file_id):
    kinds_check(kinds)
    if request.session.get('authority') >= 3 and kinds == 'office':
        return render(request, 'authority.html')
    download_file = get_object_or_404(NoticeFile, pk=file_id)
    if download_file.notice_id == Notice.objects.get(pk=notice_id):
        url = download_file.file.url
        root = str(BASE_DIR)+url

        if os.path.exists(root):
            with open(root, 'rb') as fh:
                quote_file_url = urllib.parse.quote(download_file.filename.encode('utf-8'))
                response = HttpResponse(fh.read(), content_type=mimetypes.guess_type(url)[0])
                response['Content-Disposition'] = 'attachment;filename*=UTF-8\'\'%s' % quote_file_url
                return response
            raise Http404
        else:
            raise Http404
    else:
        raise Http404

def delete(request, kinds, notice_id):
    if request.session.get('authority') != 0 and Notice.objects.get(id=notice_id).creator.id != request.session.get('user'):
        return render(request, 'authority.html')
    kinds_check(kinds)
    notice = Notice.objects.get(pk=notice_id)
    notice_file = notice.notice_file.all()
    
    if notice_file:
        for file in notice_file:
            os.remove(file.file.path)
    notice.delete()

    # edit_num = Notice.objects.filter(id__gt = notice_id)
    # for sort_num in edit_num:
    #     sort_num.num = sort_num.num-1
    #     sort_num.save()
    return redirect('/notice/{0}'.format(kinds))

def file_del(request, kinds, notice_id, file_id):
    if request.session.get('authority') != 0 and Notice.objects.get(id=notice_id).creator.id != request.session.get('user'):
        return render(request, 'authority.html')
    kinds_check(kinds)
    notice = Notice.objects.get(pk=notice_id)
    notice_file = NoticeFile.objects.get(pk=file_id)
    os.remove(notice_file.file.path)
    notice_file.delete()
    
    context = {
        'notice':notice,
        'notice_files':NoticeFile.objects.filter(notice_id=notice_id),
    }
    return redirect(reverse('notice:edit', args=(kinds, notice_id,)))

def comment_del(request, kinds, notice_id, comment_id):
    if request.session.get('authority') != 0 and Notice.objects.get(id=notice_id).creator.id != request.session.get('user'):
        return render(request, 'authority.html')
    if request.method == "POST":
        kinds_check(kinds)
        NoticeComment.objects.filter(id=comment_id).delete()

        return redirect('/notice/{0}/{1}'.format(kinds, notice_id))

    else:
        return HttpResponseNotAllowed(['POST'])

def kinds_check(kinds): # driver 나 office인지 체크
    if kinds != "driver" and kinds != "office":
        raise Http404
    return True

def approval_rule(request):
    return render(request, "notice/approval_rule.html")
def roll_call_rule(request):
    return render(request, "notice/roll_call_rule.html")
def driver_rule(request):
    return render(request, "notice/driver_rule.html")
def manager_rule(request):
    return render(request, "notice/manager_rule.html")
def field_manager_rule(request):
    return render(request, "notice/field_manager_rule.html")
def personnel_committee_rule(request):
    return render(request, "notice/personnel_committee_rule.html")

def approval_rule_print(request):
    return render(request, "notice/approval_rule_print.html")
def roll_call_rule_print(request):
    return render(request, "notice/roll_call_rule_print.html")
def driver_rule_print(request):
    return render(request, "notice/driver_rule_print.html")
def manager_rule_print(request):
    return render(request, "notice/manager_rule_print.html")
def field_manager_rule_print(request):
    return render(request, "notice/field_manager_rule_print.html")
def personnel_committee_rule_print(request):
    return render(request, "notice/personnel_committee_rule_print.html")

def organizationchart(request):
    return render(request, "notice/organizationchart.html")