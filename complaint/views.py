import json
from typing import Any

from django.db.models.query import QuerySet
from .models import Consulting, VehicleInspectionRequest, ConsultingFile, InspectionRequestFile
from humanresource.models import Member
from datetime import datetime, timedelta, date
from dispatch.models import DispatchOrder, DispatchOrderConnect, DispatchRegularlyConnect, DispatchRegularly, RegularlyGroup, DispatchRegularlyData
from django.http import JsonResponse, Http404, HttpResponse, HttpResponseNotAllowed, HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.views import generic
from django.core.exceptions import BadRequest
from config.settings import TODAY

class ConsultingList(generic.ListView):
    template_name = 'complaint/consulting.html'
    context_object_name = 'consulting_list'
    model = Consulting
    paginate_by = 10

    def get(self, request, *args, **kwargs):
        if request.session.get('authority') >= 3:
            return render(request, 'authority.html')
        return super().get(request, *args, **kwargs)

    def get_queryset(self):
        date1 = self.request.GET.get('date1', TODAY)
        date2 = self.request.GET.get('date2', TODAY)
        date1 = f'{date1} 00:00'
        date2 = f'{date2} 24:00'
        name = self.request.GET.get('name')
        role = self.request.GET.get('role', '담당업무')

        if date1 > date2:
            raise Http404
        consulting_list = Consulting.objects.select_related('member_id').filter(date__gte=date1).filter(date__lte=date2).order_by('-pub_date')

        if name:
            consulting_list = consulting_list.filter(member_id__name=name)
        if role != '담당업무':
            consulting_list = consulting_list.filter(member_id__role=role)
        self.num = consulting_list.count()
        return consulting_list

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
        #페이징 끝

        context['num'] = self.num - (current_page - 1) * 10
        context['date1'] = self.request.GET.get('date1', TODAY)
        context['date2'] = self.request.GET.get('date2', TODAY)
        context['name'] = self.request.GET.get('name', '')
        context['role'] = self.request.GET.get('role', '담당업무')
        return context

def consulting_edit(request):
    if request.method == 'POST':
        user_auth = request.session.get('authority')
        if user_auth >= 3:
            return render(request, 'authority.html')

        consulting_list = request.POST.getlist('check')
        status_list = request.POST.getlist('status')
        editor = get_object_or_404(Member, pk=request.session.get('user'))

        for pk, status in zip(consulting_list, status_list):
            consulting = get_object_or_404(Consulting, pk=pk)
            consulting.status = status
            consulting.check_member_id = editor
            consulting.save()
        return redirect(request.META.get('HTTP_REFERER', 'redirect_if_referer_not_found'))
    else:
        return HttpResponseNotAllowed(['post'])

def consulting_delete(request):
    if request.method == 'POST':
        user_auth = request.session.get('authority')
        if user_auth >= 3:
            return render(request, 'authority.html')

        del_list = request.POST.getlist('check', '')
        
        for pk in del_list:
            consulting = get_object_or_404(Consulting, pk=pk)
            consulting.delete()

        return redirect(request.META.get('HTTP_REFERER', 'redirect_if_referer_not_found'))
    else:
        return HttpResponseNotAllowed(['post'])

def consulting_image(request, id):
    consulting = get_object_or_404(Consulting, id=id)
    images = consulting.consulting_file.all()
    context = {
        'images': images
    }
    return render(request, 'complaint/imgview.html', context)


class InspectionList(generic.ListView):
    template_name = 'complaint/inspection.html'
    context_object_name = 'inspection_list'
    model = VehicleInspectionRequest
    paginate_by = 10

    def get(self, request, *args, **kwargs):
        if request.session.get('authority') >= 3:
            return render(request, 'authority.html')
        return super().get(request, *args, **kwargs)

    def get_queryset(self):
        date1 = self.request.GET.get('date1', TODAY)
        date2 = self.request.GET.get('date2', TODAY)
        date1 = f'{date1} 00:00'
        date2 = f'{date2} 24:00'
        name = self.request.GET.get('name')
        role = self.request.GET.get('role', '담당업무')

        if date1 > date2:
            raise Http404
        inspection_list = VehicleInspectionRequest.objects.select_related('member_id').filter(date__gte=date1).filter(date__lte=date2).order_by('-pub_date')

        if name:
            inspection_list = inspection_list.filter(member_id__name=name)
        if role != '담당업무':
            inspection_list = inspection_list.filter(member_id__role=role)
        self.num = inspection_list.count()
        return inspection_list

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
        #페이징 끝

        context['num'] = self.num - (current_page - 1) * 10
        context['date1'] = self.request.GET.get('date1', TODAY)
        context['date2'] = self.request.GET.get('date2', TODAY)
        context['name'] = self.request.GET.get('name', '')
        context['role'] = self.request.GET.get('role', '담당업무')
        return context

def inspection_edit(request):
    if request.method == 'POST':
        user_auth = request.session.get('authority')
        if user_auth >= 3:
            return render(request, 'authority.html')

        inspection_list = request.POST.getlist('check')
        status_list = request.POST.getlist('status')
        editor = get_object_or_404(Member, pk=request.session.get('user'))

        for pk, status in zip(inspection_list, status_list):
            inspection = get_object_or_404(VehicleInspectionRequest, pk=pk)
            inspection.status = status
            inspection.check_member_id = editor
            inspection.save()
        return redirect(request.META.get('HTTP_REFERER', 'redirect_if_referer_not_found'))
    else:
        return HttpResponseNotAllowed(['post'])

def inspection_delete(request):
    if request.method == 'POST':
        user_auth = request.session.get('authority')
        if user_auth >= 3:
            return render(request, 'authority.html')

        del_list = request.POST.getlist('check', '')
        
        for pk in del_list:
            inspection = get_object_or_404(VehicleInspectionRequest, pk=pk)
            inspection.delete()

        return redirect(request.META.get('HTTP_REFERER', 'redirect_if_referer_not_found'))
    else:
        return HttpResponseNotAllowed(['post'])


def inspection_image(request, id):
    inspection = get_object_or_404(VehicleInspectionRequest, id=id)
    images = inspection.inspection_request_file.all()
    context = {
        'images': images
    }
    return render(request, 'complaint/imgview.html', context)

class Grievance(generic.ListView):
    template_name = 'complaint/grievance.html'
    context_object_name = 'member_list'
    model = Member
    authority_level = 3

    def get(self, request, *args, **kwargs):
        members = self.model.objects.all()
        context = {
            self.context_object_name: members
        }
        return render(request, self.template_name, context)