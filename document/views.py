import urllib
import os
import mimetypes
from django.http import JsonResponse, Http404, HttpResponse, HttpResponseNotAllowed
from django.views import generic
from django.shortcuts import render, redirect, get_object_or_404
from dispatch.models import DispatchOrder
from humanresource.models import Member
from .models import Document, DocumentGroup
from datetime import datetime, timedelta, date
from config.settings import BASE_DIR

TODAY = str(datetime.now())[:10]
FORMAT = "%Y-%m-%d"


class CompanyDocumentList(generic.ListView):
    template_name = 'document/company.html'
    context_object_name = 'group_list'
    model = DocumentGroup

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        file_list = ''
        filename = self.request.GET.get('filename', '')
        if filename:
            group_list = []
            file_list = Document.objects.select_related('group_id').filter(filename__contains=filename)
            for file in file_list:
                group_list.append(file.group_id)
            
            group_list = list(set(group_list))
            context['group_list'] = group_list

        context['search'] = filename
        context['file_list'] = file_list
        return context

def company_document_create(request):
    upload_file = request.FILES.get('file')
    filename = request.POST.get('filename')
    group_id = get_object_or_404(DocumentGroup, id=request.POST.get('group_id'))


    file = Document(
        group_id=group_id,
        file=upload_file,
        filename=filename,
        creator = get_object_or_404(Member, pk=request.session.get('user')),
    )
    file.save()
    return redirect(request.META.get('HTTP_REFERER', 'redirect_if_referer_not_found'))


def company_group_create(request):
    
    group_name = request.POST.get('group_name')
    
    group = DocumentGroup(
        name = group_name,
        creator = get_object_or_404(Member, pk=request.session.get('user')),
    )
    group.save()
    return redirect(request.META.get('HTTP_REFERER', 'redirect_if_referer_not_found'))

def company_document_download(request, id):
    download_file = get_object_or_404(Document, pk=id)

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

def company_delete(request):
    file_list = request.POST.getlist('file_check')
    group_list = request.POST.getlist('group_check')

    for file_id in file_list:
        file = get_object_or_404(Document, id=file_id)
        if file.file:
            os.remove(file.file.path)
        file.delete()

    return redirect(request.META.get('HTTP_REFERER', 'redirect_if_referer_not_found'))

def company_group_delete(request):
    
    id = request.POST.get('id')
    group = get_object_or_404(DocumentGroup, id=id)
    document_list = group.group_file.all()
    for document in document_list:
        os.remove(document.file.path)
        document.delete()
    group.delete()
    
    return redirect(request.META.get('HTTP_REFERER', 'redirect_if_referer_not_found'))

def company_group_edit(request):
    name = request.POST.get('name')
    id = request.POST.get('id')

    group = get_object_or_404(DocumentGroup, id=id)
    group.name = name
    group.save()


    return redirect(request.META.get('HTTP_REFERER', 'redirect_if_referer_not_found'))
# def download(request, kinds, notice_id, file_id):
#     kinds_check(kinds)
#     download_file = get_object_or_404(NoticeFile, pk=file_id)
#     if download_file.notice_id == Notice.objects.get(pk=notice_id):
#         url = download_file.file.url
#         root = str(BASE_DIR)+url
#         print("\n테스트\n", root)

#         if os.path.exists(root):
#             with open(root, 'rb') as fh:
#                 quote_file_url = urllib.parse.quote(download_file.filename.encode('utf-8'))
#                 response = HttpResponse(fh.read(), content_type=mimetypes.guess_type(url)[0])
#                 response['Content-Disposition'] = 'attachment;filename*=UTF-8\'\'%s' % quote_file_url
#                 return response
#             raise Http404
#         else:
#             print("에러")
#             raise Http404
#     else:
#         raise Http404

class DocumentList(generic.ListView):
    template_name = 'document/document.html'
    context_object_name = 'order_list'
    model = DispatchOrder

    def get_queryset(self):
        date1 = self.request.GET.get('date1', TODAY)
        date2 = self.request.GET.get('date2', TODAY)
        route = self.request.GET.get('route')
        
        order_list = DispatchOrder.objects.prefetch_related('info_order').exclude(arrival_date__lt=f'{date1} 00:00').exclude(departure_date__gt=f'{date2} 24:00').exclude(contract_status='취소').order_by('departure_date')
        if route:
            order_list = order_list.filter(route__contains=route).order_by('departure_date')
        return order_list

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['route'] = self.request.GET.get('route', '')
        
        
        connect_list = []
        for order in context['order_list']:
            connect_list.append(order.info_order.all())
        context['connect_list'] = connect_list
        
        context['date1'] = self.request.GET.get('date1', TODAY)
        context['date2'] = self.request.GET.get('date2', TODAY)
        
        return context

def vehicle_print(request):
    id = request.GET.get('id')
    order = get_object_or_404(DispatchOrder, id=id)
    file_list = []
    for connect in order.info_order.all():

        file = connect.bus_id.vehicle_file.all()
        if file.exists():
            file_list.append(file.get(type='차량등록증'))

    

    return render(request, 'document/vehicle_print.html', {'file_list': file_list})

def commitment_print(request):
    id = request.GET.get('id')
    order = get_object_or_404(DispatchOrder, id=id)
    connect_list_all = order.info_order.all()
    cut = False
    connect_list = connect_list_all
    connect_list2 = ''
    if len(connect_list_all) > 18:
        cut = True
        connect_list = connect_list_all[:18]
        connect_list2 = connect_list_all[18:]
    
    return render(request, 'document/commitment_print.html', {'connect_list': connect_list, 'connect_list2': connect_list2, 'order': order, 'cut': cut})

def safety_print(request):
    id = request.GET.get('id')
    order = get_object_or_404(DispatchOrder, id=id)
    connect_list = order.info_order.all()

    return render(request, 'document/safety_print.html', {'connect_list': connect_list, 'order': order})

def school_print(request):
    id = request.GET.get('id')
    order = get_object_or_404(DispatchOrder, id=id)

    return render(request, 'document/school_print.html', {'order': order})

def drinking_print(request):
    id = request.GET.get('id')
    order = get_object_or_404(DispatchOrder, id=id)
    connect_list = order.info_order.all()

    
    return render(request, 'document/drinking_print.html', {'connect_list': connect_list, 'departure_date': order.departure_date[:10], 'order': order})
