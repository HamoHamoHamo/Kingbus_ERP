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
