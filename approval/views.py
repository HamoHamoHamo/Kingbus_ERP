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
from .forms import ApprovalForm, ApproverForm
from .models import Approver, Approval

# Create your views here.

class ApprovalList(generic.ListView):
    template_name = 'approval/approval.html'
    context_object_name = 'approval_list'
    model = Approval
    paginate_by = 10

    def get_queryset(self) -> QuerySet[Any]:
        date1 = self.request.GET.get("date1", f"{add_days_to_date(f'{TODAY[:7]}-01', -1)[:7]}-01")
        date2 = self.request.GET.get("date1", f"{TODAY} 23:59")
        search = self.request.GET.get("search", '')

        date1 = datetime.strptime(date1, FORMAT)
        date2 = datetime.strptime(date2, DATE_TIME_FORMAT)

        if search:
            search_type = self.request.GET.get("search_type", '')
            status = self.request.GET.get("status", '')
            if search_type == '제목':
                if status == "전체":
                    approval_list = Approval.objects.filter(title="search", pub_date__range=[date1, date2])
                else:
                    approval_list = Approval.objects.filter(title="search", status=status, pub_date__range=[date1, date2])
            elif search_type == "결재자":
                approver = Approver.objects.filter(member_id__name=search)
                if status == "전체":
                    approval_list = Approval.objects.filter(approver=approver[0], pub_date__range=[date1, date2])
                else:
                    approval_list = Approval.objects.filter(status=status, approver=approver[0], pub_date__range=[date1, date2])
        else:
            approval_list = Approval.objects.filter(pub_date__range=[date1, date2])

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
        context['date2'] = self.request.GET.get("date1", TODAY)

        context['approver_list'] = []
        for approval in context['approval_list']:
            context['approver_list'].append(approval.approver.order_by("index").last().creator.name)
        
        return context

class ApprovalDetail(generic.DetailView):
    template_name = 'approval/approval_detail.html'
    context_object_name = 'approval'
    model = Approval

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        context['approver_select_list'] = set_approver_select()
        context['approver_list'] = []
        context['approver_list'] = context['approval'].approver.order_by("index").last().creator.name
        context['pub_date'] = datetime.strftime(context['approval'].pub_date, DATE_TIME_FORMAT)
        
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
            approval.save()

            # 결재자 지정
            create_next_approver(approval, next_approver, 1)
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
        creator = get_object_or_404(Member, id=request.session.get('user'))
        approval = get_object_or_404(Approval, id=request.POST.get("id"))
        authority = request.session.get('authority')

        if creator == approval.creator or authority <= 2:
            approval.delete()
    return redirect(request.META.get('HTTP_REFERER', 'redirect_if_referer_not_found'))

def approver_create(request):
    if request.method == "POST":
        approver_form = ApproverForm(request.POST)
        
        if approver_form.is_valid():
            approval_id = request.POST.get('approval_id')
            next_approver = get_object_or_404(Member, id=request.POST.get("next_approver"))
            approval = get_object_or_404(Approval, id=approval_id)
            creator = get_object_or_404(Member, id=request.session.get('user'))
            approver = approver_form.save(commit=False)

            approver.approval_id = approval
            approver.creator = creator
            approver.save()
            
            if approver.status == "승인" and next_approver:
                create_next_approver(approval, next_approver, approver.index + 1)
                approval.status = "처리중"
            else:
                approval.status = approver.status
            approval.save()

            return redirect(request.META.get('HTTP_REFERER', 'redirect_if_referer_not_found'))
        else:
            raise Http404
    else:
        return HttpResponseNotAllowed(['POST'])

def create_next_approver(approval, next_approver, index):
    Approver.objects.create(
        approval_id = approval,
        creator = next_approver,
        index = index
    )

def approver_edit(request):
    if request.method == "POST":
        approver = get_object_or_404(Approver, id=request.POST.get("id"))
        if approver.status == "처리중":
            approver.content = request.POST.get("content")
            approver.save()
        
        return redirect(request.META.get('HTTP_REFERER', 'redirect_if_referer_not_found'))
    else:
        return HttpResponseNotAllowed(['POST'])
    
class ApprovalProcess(generic.ListView):
    template_name = 'approval/approval_process.html'
    context_object_name = 'member_list'
    model = Member

    def get(self, request, *args, **kwargs):
        members = self.model.objects.all()
        context = {
            self.context_object_name: members
        }
        return render(request, self.template_name, context)