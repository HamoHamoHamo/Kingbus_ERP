from django.shortcuts import render
from django.views import generic
from humanresource.models import Member


# Create your views here.
class Management(generic.ListView):
    template_name = 'rollcall/management.html'
    context_object_name = 'member_list'
    model = Member
    authority_level = 3

    def get(self, request, *args, **kwargs):
        members = self.model.objects.all()
        context = {
            self.context_object_name: members
        }
        return render(request, self.template_name, context)
        