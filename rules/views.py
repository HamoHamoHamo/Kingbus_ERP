from django.shortcuts import render
from django.views import generic
from humanresource.models import Member

# Create your views here.

class ApprovalRules(generic.ListView):
    template_name = 'rules/approvalrules.html'
    context_object_name = 'member_list'
    model = Member
    authority_level = 3

    def get(self, request, *args, **kwargs):
        members = self.model.objects.all()
        context = {
            self.context_object_name: members
        }
        return render(request, self.template_name, context)

class RowCallRules(generic.ListView):
    template_name = 'rules/rowcallrules.html'
    context_object_name = 'member_list'
    model = Member
    authority_level = 3

    def get(self, request, *args, **kwargs):
        members = self.model.objects.all()
        context = {
            self.context_object_name: members
        }
        return render(request, self.template_name, context)

class DriverRules(generic.ListView):
    template_name = 'rules/driverrules.html'
    context_object_name = 'member_list'
    model = Member
    authority_level = 3

    def get(self, request, *args, **kwargs):
        members = self.model.objects.all()
        context = {
            self.context_object_name: members
        }
        return render(request, self.template_name, context)
    
class ManagerRules(generic.ListView):
    template_name = 'rules/managerrules.html'
    context_object_name = 'member_list'
    model = Member
    authority_level = 3

    def get(self, request, *args, **kwargs):
        members = self.model.objects.all()
        context = {
            self.context_object_name: members
        }
        return render(request, self.template_name, context)
    
class FieldManagerRules(generic.ListView):
    template_name = 'rules/fieldmanagerrules.html'
    context_object_name = 'member_list'
    model = Member
    authority_level = 3

    def get(self, request, *args, **kwargs):
        members = self.model.objects.all()
        context = {
            self.context_object_name: members
        }
        return render(request, self.template_name, context)

class PersonnelCommittee(generic.ListView):
    template_name = 'rules/personnelcommittee.html'
    context_object_name = 'member_list'
    model = Member
    authority_level = 3

    def get(self, request, *args, **kwargs):
        members = self.model.objects.all()
        context = {
            self.context_object_name: members
        }
        return render(request, self.template_name, context)

class ItemManagement(generic.View):
    template_name = 'rules/Itemmanagement.html'

    def get(self, request, *args, **kwargs):
        rows = [
            {
                'checkbox': '<input type="checkbox" />',
                'department': '경영 관리과',
                'sub_department': '회계부',
                'task': '결재 (대출이자, 공제조합출납표, 차량할부금 정리)',
                'daily_price': '500',
                'monthly_price': '500,000',
                'responsible': '고영이 / 최정이',
                'position': '과장',
                'approval_line': '전조출',
            },
            # 다른 데이터들도 동일하게 추가
            {
                'checkbox': '<input type="checkbox" />',
                'department': '경영 관리과',
                'sub_department': '배차부',
                'task': '결재 (대출이자, 공제조합출납표, 차량할부금 정리)',
                'daily_price': '500',
                'monthly_price': '500,000',
                'responsible': '고영이 / 최정이',
                'position': '과장',
                'approval_line': '전조출',
            },
            {
                'checkbox': '<input type="checkbox" />',
                'department': '경영 관리과',
                'sub_department': '배차부',
                'task': '결재 (대출이자, 공제조합출납표, 차량할부금 정리)',
                'daily_price': '500',
                'monthly_price': '500,000',
                'responsible': '고영이 / 최정이',
                'position': '과장',
                'approval_line': '김형주',
            },
            # 계속해서 추가
        ]
        context = {'rows': rows}
        return render(request, self.template_name, context)

class OrganizationChart(generic.ListView):
    template_name = 'rules/organizationchart.html'
    context_object_name = 'member_list'
    model = Member
    authority_level = 3

    def get(self, request, *args, **kwargs):
        members = self.model.objects.all()
        context = {
            self.context_object_name: members
        }
        return render(request, self.template_name, context)