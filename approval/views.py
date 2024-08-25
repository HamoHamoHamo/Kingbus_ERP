import os
from typing import Any
from common.datetime import add_days_to_date
from common.constant import TODAY, FORMAT, WEEK, WEEK2, DATE_TIME_FORMAT
from django.db.models.query import QuerySet
from django.shortcuts import render
from django.views import generic
from humanresource.models import Member
from config.settings import MEDIA_ROOT
from django.db.models import Q, Sum
from django.forms.models import model_to_dict
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned, BadRequest
from django.http import Http404, JsonResponse, HttpResponse, HttpResponseNotAllowed
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.views import generic
from datetime import datetime
from media_firebase import upload_to_firebase, get_download_url, delete_firebase_file
from my_settings import CRED_PATH, CLOUD_MEDIA_PATH
from .forms import ApprovalForm, ApproverForm
from .models import Approver, Approval, ApprovalFile

# Create your views here.

class ApprovalList(generic.ListView):
    template_name = 'approval/approval.html'
    context_object_name = 'approval_list'
    model = Approval
    paginate_by = 10

    def get_queryset(self) -> QuerySet[Any]:
        date1 = self.request.GET.get("date1", f"{add_days_to_date(f'{TODAY[:7]}-01', -1)[:7]}-01")
        date2 = self.request.GET.get("date2", TODAY)
        search = self.request.GET.get("search", None)
        status = self.request.GET.get("status", "전체")

        # date1 = datetime.strptime(date1, FORMAT)
        # date2 = datetime.strptime(date2, FORMAT)

        if status != "전체":
            print("1")
            approval_list = Approval.objects.filter(status=status, pub_date__range=[f"{date1} 00:00", f"{date2} 23:59"])
        else:
            print("2")
            approval_list = Approval.objects.filter(pub_date__range=[f"{date1} 00:00", f"{date2} 23:59"])

        if search:
            print("3")
            search_type = self.request.GET.get("search_type", '')
            if search_type == '제목':
                approval_list = approval_list.filter(title__contains=search)                
            elif search_type == "결재자":
                approval_list = approval_list.filter(current_approver_name__contains=search)
        print("ETST", approval_list)
        return approval_list.order_by('-pub_date')

    
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
        
        context['search'] = self.request.GET.get('search', '')
        context['selector'] = self.request.GET.get('top_box_selector', 'title')
        context['date1'] = self.request.GET.get("date1", f"{add_days_to_date(f'{TODAY[:7]}-01', -1)[:7]}-01")
        context['date2'] = self.request.GET.get("date2", TODAY)
        context['search_type'] = self.request.GET.get("search_type", '')
        context['status'] = self.request.GET.get("status", '전체')


        context['approver_list'] = []
        context['file_list'] = []
        for approval in context['approval_list']:
            context['approver_list'].append(approval.approver.order_by("index").last().creator.name)
            context['file_list'].append(list(approval.approval_file.values_list("filename")))
        

        return context

class ApprovalDetail(generic.DetailView):
    template_name = 'approval/approval_detail.html'
    context_object_name = 'approval'
    model = Approval

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        login_user = get_object_or_404(Member, id=self.request.session.get('user'))
        
        context['approver_select_list'] = set_approver_select()
        context['last_approver'] = context['approval'].approver.filter(status="").order_by("index").last()
        last_approver_id = context['last_approver'].id if context['last_approver'] else 0
        context['approver_list'] = context['approval'].approver.exclude(id=last_approver_id).order_by("index")
        
        context['pub_date'] = datetime.strftime(context['approval'].pub_date, DATE_TIME_FORMAT)
        context['can_approve'] = True if context['last_approver'] and login_user == context['last_approver'].creator or login_user.role == "최고관리자" else False
        context['can_add_approver'] = True if len(context['approver_list']) < 3 and (context['approval'].status == "대기" or context['approval'].status == "처리중") else False

        return context
    
    
def set_approver_select():
    approver_select_list = []
    approver_select_list.append(Member.objects.filter(use="사용").get(name="고영이"))
    approver_select_list.append(Member.objects.filter(use="사용").get(name="이세명"))
    approver_select_list.append(Member.objects.filter(use="사용").get(name="김인숙"))
    approver_select_list.append(Member.objects.filter(use="사용").get(name="김형주"))
    approver_select_list.append(Member.objects.filter(use="사용").get(name="엄성환"))
    approver_select_list.append(Member.objects.filter(use="사용").get(name="김성태"))
    return approver_select_list

def approval_create(request):
    if request.method == "GET":
        context = {}
        context['approver_select_list'] = set_approver_select()
        return render(request, "approval/approval_create.html", context)

    if request.method == "POST":
        approval_form = ApprovalForm(request.POST)
        
        if approval_form.is_valid():
            next_approver = get_object_or_404(Member, id=request.POST.get("next_approver"))
            creator = get_object_or_404(Member, id=request.session.get('user'))
            approval = approval_form.save(commit=False)
            approval.creator = creator
            approval.date = TODAY[:10]
            approval.status = '대기'
            approval.current_approver_name = next_approver.name
            approval.save()

            # 결재자 지정
            create_next_approver(approval, next_approver, 1)
            approval_file_upload(request, approval.id)
            return redirect(reverse('approval:approval'))
        else:
            raise BadRequest(f"{approval_form.errors}")
    else:
        return HttpResponseNotAllowed(['POST', 'GET'])

def approval_edit(request):
    if request.method == "POST":
        creator = get_object_or_404(Member, id=request.session.get('user'))

        approval = get_object_or_404(Approval, id=request.POST.get("id"))
        if approval.creator != creator:
            raise BadRequest("작성자만 수정할 수 있습니다.")
        if approval.status != "대기":
            raise BadRequest("대기 상태일 때만 수정할 수 있습니다.")
        approval_form = ApprovalForm(request.POST, instance=approval)
        
        if approval_form.is_valid():
            creator = get_object_or_404(Member, id=request.session.get('user'))
            approval = approval_form.save(commit=False)
            approval.creator = creator
            approval.date = TODAY
            approval.save()
            return redirect(reverse('approval:approval'))
        else:
            raise Http404
    else:
        return HttpResponseNotAllowed(['POST'])

def approval_delete(request):
    if request.method == "POST":
        login_user = get_object_or_404(Member, id=request.session.get('user'))
        approval_id_list = request.POST.getlist("delete_id")
        authority = request.session.get('authority')

        approval_list = []
        for id in approval_id_list:
            approval = get_object_or_404(Approval, id=id)
            approval_list.append(approval)
            if not (login_user == approval.creator or authority <= 2):
                raise BadRequest("작성자 또는 관리자만 삭제할 수 있습니다.")
        for approval in approval_list:
            approval.delete()

    return redirect(request.META.get('HTTP_REFERER', 'redirect_if_referer_not_found'))

def approver_edit(request):
    if request.method == "POST":
        approver = get_object_or_404(Approver, id=request.POST.get("approver"))
        approval = approver.approval_id
        status = request.POST.get('status')
        content = request.POST.get('content')
        approver.status = status
        approver.content = content

        if request.POST.get("next_approver"):
            next_approver = get_object_or_404(Member, id=request.POST.get("next_approver"))
            create_next_approver(approval, next_approver, approver.index + 1)
            approval.status = "처리중"
            approval.current_approver_name = next_approver.name
            approval.save()
        else:
            approval.status = status
            approval.save()
        approver.save()
        return redirect(request.META.get('HTTP_REFERER', 'redirect_if_referer_not_found'))

        # approver_form = ApproverForm(request.POST)
    
        # if approver_form.is_valid():
        #     approval_id = request.POST.get('approval_id')
        #     next_approver = get_object_or_404(Member, id=request.POST.get("next_approver"))
        #     approval = get_object_or_404(Approval, id=approval_id)
        #     creator = get_object_or_404(Member, id=request.session.get('user'))
        #     approver = approver_form.save(commit=False)

        #     approver.approval_id = approval
        #     approver.creator = creator
        #     approver.save()
            
        #     if approver.status == "승인" and next_approver:
        #         create_next_approver(approval, next_approver, approver.index + 1)
        #         approval.status = "처리중"
        #     else:
        #         approval.status = approver.status
        #     approval.save()

        #     return redirect(request.META.get('HTTP_REFERER', 'redirect_if_referer_not_found'))
        # else:
        #     raise Http404
    else:
        return HttpResponseNotAllowed(['POST'])

def create_next_approver(approval, next_approver, index):
    Approver.objects.create(
        approval_id = approval,
        creator = next_approver,
        index = index
    )

# def approver_edit(request):
#     if request.method == "POST":
#         approver = get_object_or_404(Approver, id=request.POST.get("id"))
#         if approver.status == "처리중":
#             approver.content = request.POST.get("content")
#             approver.save()
        
#         return redirect(request.META.get('HTTP_REFERER', 'redirect_if_referer_not_found'))
#     else:
#         return HttpResponseNotAllowed(['POST'])
    
def approval_file_upload(request, id):
    creator = Member.objects.get(pk=request.session.get('user'))
    approval = get_object_or_404(Approval, id=id)

    
    request_file_list = request.FILES.getlist("file", None)
    for request_file in request_file_list:
        file = ApprovalFile(
            approval_id=approval,
            file=request_file,
            filename=request_file.name,
            creator=creator,
        )
        file.save()
        try:
            file_path = f'{CLOUD_MEDIA_PATH}{file.file}_{file.filename}'
            upload_to_firebase(file, file_path)
            file.path = file_path
            file.save()
            os.remove(file.file.path)
        except Exception as e:
            print("Firebase upload error", e)
            #파이어베이스 업로드 실패 시 파일 삭제
            os.remove(file.file.path)
            file.delete()

            return False
    return True

def approval_file_download(request, pk):
    user_auth = request.session.get('authority')
    if user_auth >= 3:
        return render(request, 'authority.html')
    
    approval = get_object_or_404(Approval, id=pk)

    url_list = []
    file_list = approval.approval_file.all()
    for file in file_list:
        url_list.append(get_download_url(file.path))

    context = {
        'url_list' : url_list
    }
    return render(request, 'approval/approval_img.html', context)