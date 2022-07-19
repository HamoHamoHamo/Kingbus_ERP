import urllib
import os
import mimetypes
from datetime import datetime
from django.db.models import Q
from django.shortcuts import render, redirect, get_object_or_404
from django.http import Http404, HttpResponse, HttpResponseNotAllowed
from django.views import generic
from django.urls import reverse
from .models import Vehicle, VehicleDocument
from .forms import VehicleForm
from humanresource.models import Member
from ERP.settings import BASE_DIR
from dateutil.relativedelta import relativedelta

TODAY = str(datetime.now())[:10]
FORMAT = "%Y-%m-%d"

def document_image(request, file_id):
    context = {
        'img': get_object_or_404(VehicleDocument, id=file_id)
    }
    return render(request, 'vehicle/document_img.html', context)

class VehicleMgmt(generic.ListView):
    template_name = 'vehicle/mgmt.html'
    context_object_name = 'vehicle_list'
    model = Vehicle

    def get_queryset(self):
        select = self.request.GET.get('select', None)
        search = self.request.GET.get('search', None)
        
        # q = Q()
        if not search:
            vehicle = Vehicle.objects.order_by('-use', '-pk')
        else:
            if select == 'vehicle':
                vehicle = Vehicle.objects.filter(vehicle_num=search).order_by('-use', '-pk')
            elif select == 'driver':
                vehicle = Vehicle.objects.filter(driver_name=search).order_by('-use', '-pk')
            elif select == 'passenger':
                vehicle = Vehicle.objects.filter(passenger_num=search).order_by('-use', '-pk')
        return vehicle
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        #만료일 1달 전부터 보여주기 = today + 1달 보다 작을때
        i_next_month = datetime.strptime(TODAY, FORMAT) + relativedelta(months=1)
        i_next_month = i_next_month.strftime(FORMAT)
        context['insurance_list'] = context['vehicle_list'].filter(insurance_expiry_date__gt='').filter(insurance_expiry_date__lte=i_next_month).order_by('insurance_expiry_date')

        file_list = []
        for vehicle in context['insurance_list']:
            files = VehicleDocument.objects.filter(vehicle_id=vehicle)
            
            try:
                i_file = files.get(type="insurance_receipt")
                file_list.append(i_file)
            except:
                file_list.append('')
        context['file_list'] = file_list


        #검사유효기간 11달 후부터 보여주기 = today -11달 보다 작을때
        c_next_month = datetime.strptime(TODAY, FORMAT) - relativedelta(months=11)
        c_next_month = c_next_month.strftime(FORMAT)
        
        context['check_list'] = context['vehicle_list'].filter(check_duration__lte=c_next_month).order_by('check_duration')
        
        duration = []
        expire = []

        for vehicle in context['check_list']:
            month = datetime.strptime(vehicle.check_duration, FORMAT) + relativedelta(years=1)
            year = month + relativedelta(months=1)
            month = month.strftime(FORMAT)
            year = year.strftime(FORMAT)

            duration.append(month)
            expire.append(year)
        context['duration'] = duration
        context['expire'] = expire

        context['select'] = self.request.GET.get('select', '')
        context['search'] = self.request.GET.get('search', '')

        return context



class VehicleList(generic.ListView):
    template_name = 'vehicle/list.html'
    context_object_name = 'vehicle_list'
    model = Vehicle
    paginate_by = 10

    def get_queryset(self):
        select = self.request.GET.get('select', None)
        search = self.request.GET.get('search', None)
        
        # q = Q()
        if not search:
            vehicle = Vehicle.objects.order_by('-use', '-pk')
        else:
            if select == 'vehicle':
                vehicle = Vehicle.objects.filter(vehicle_num=search).order_by('-use', '-pk')
            elif select == 'driver':
                vehicle = Vehicle.objects.filter(driver_name=search).order_by('-use', '-pk')
            elif select == 'passenger':
                vehicle = Vehicle.objects.filter(passenger_num=search).order_by('-use', '-pk')
        return vehicle


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

        context['select'] = self.request.GET.get('select', '')
        context['search'] = self.request.GET.get('search', '')
        context['driver_list'] = Member.objects.filter(role='운전원')
        
        file_list = []
        for vehicle in context['vehicle_list']:
            files = VehicleDocument.objects.filter(vehicle_id=vehicle)
            list = []
            try:
                v_file = files.get(type="vehicle_registration")
                list.append(v_file)
            except:
                list.append('')
            try:
                i_file = files.get(type="insurance_receipt")
                list.append(i_file)
            except:
                list.append('')
            file_list.append(list)
        context['file_list'] = file_list

        return context


def vehicle_create(request):
    if request.method == 'POST':
        vehicle_form = VehicleForm(request.POST)

        if vehicle_form.is_valid():            
            driver = get_object_or_404(Member, pk=request.POST.get('driver'))
            vehicle_registration_file = request.FILES.get('vehicle_registration', None)
            insurance_receipt_file = request.FILES.get('insurance_receipt', None)
            
            vehicle = vehicle_form.save(commit=False)
            vehicle.driver = driver
            vehicle.driver_name = driver.name
            vehicle.save()
            if vehicle_registration_file:
                vehicle_file_save(vehicle_registration_file, vehicle, "vehicle_registration")

            if insurance_receipt_file:
                vehicle_file_save(insurance_receipt_file, vehicle, "insurance_receipt")

            return redirect('vehicle:list')
        else:
            return Http404

    else:
        return HttpResponseNotAllowed(['post'])

def vehicle_edit(request):
    pk = request.POST.get('id', None)
    vehicle = get_object_or_404(Vehicle, pk=pk)

    if request.method == 'POST':
        vehicle_form = VehicleForm(request.POST)
        #insurance_form = VehicleInsuranceForm(request.POST)
        #if vehicle_form.is_valid() and insurance_form.is_valid():
        if vehicle_form.is_valid():
            vehicle.driver = get_object_or_404(Member, id=request.POST.get('driver', None))
            vehicle.driver_name = vehicle.driver.name

            vehicle.vehicle_num0 = vehicle_form.cleaned_data['vehicle_num0']
            vehicle.vehicle_num = vehicle_form.cleaned_data['vehicle_num']
            vehicle.vehicle_id = vehicle_form.cleaned_data['vehicle_id']
            vehicle.motor_type = vehicle_form.cleaned_data['motor_type']
            vehicle.rated_output = vehicle_form.cleaned_data['rated_output']
            vehicle.vehicle_type = vehicle_form.cleaned_data['vehicle_type']
            vehicle.maker = vehicle_form.cleaned_data['maker']
            vehicle.model_year = vehicle_form.cleaned_data['model_year']
            vehicle.release_date = vehicle_form.cleaned_data['release_date']
            vehicle.use = vehicle_form.cleaned_data['use']
            vehicle.passenger_num = vehicle_form.cleaned_data['passenger_num']
            vehicle.check_duration = vehicle_form.cleaned_data['check_duration']
            vehicle.insurance_expiry_date = vehicle_form.cleaned_data['insurance_expiry_date']
            vehicle.save()

            # 파일
            vehicle_file = request.FILES.get('vehicle_registration', None)
            insurance_file = request.FILES.get('insurance_receipt', None)
            v_file_name = request.POST.get('vehicle_registration_name', None)
            i_file_name = request.POST.get('insurance_receipt_name', None)

            cur_files = VehicleDocument.objects.filter(vehicle_id=vehicle)
            try:
                cur_vehicle_files = cur_files.get(type='vehicle_registration')
            except:
                cur_vehicle_files = None
            try:
                cur_insurance_files = cur_files.get(type='insurance_receipt')
            except:
                cur_insurance_files = None

            if vehicle_file:
                if cur_vehicle_files:
                    os.remove(cur_vehicle_files.file.path)
                    cur_vehicle_files.delete()
                file = VehicleDocument(
                    vehicle_id=vehicle,
                    file=vehicle_file,
                    filename=vehicle_file.name,
                    type='vehicle_registration',
                )
                file.save()
            elif not v_file_name and cur_vehicle_files:
                os.remove(cur_vehicle_files.file.path)
                cur_vehicle_files.delete()

            if insurance_file:
                if cur_insurance_files:
                    os.remove(cur_insurance_files.file.path)
                    cur_insurance_files.delete()

                file = VehicleDocument(
                    vehicle_id=vehicle,
                    file=insurance_file,
                    filename=insurance_file.name,
                    type='insurance_receipt',
                )
                file.save()
            elif not i_file_name and cur_insurance_files:
                os.remove(cur_insurance_files.file.path)
                cur_insurance_files.delete()
                
            return redirect('vehicle:list')
        else:
            Http404
    raise Http404


def vehicle_delete(request):
    if request.method == 'POST':
        pk_list = request.POST.getlist('check',None)
        for pk in pk_list:
            vehicle = get_object_or_404(Vehicle, pk=pk)
            #insurance = get_object_or_404(VehicleInsurance, vehicle_id=pk)
            #document = get_object_or_404(VehicleDocument, vehicle_id=pk)
            documents = VehicleDocument.objects.filter(vehicle_id=vehicle)
            for file in documents:
                os.remove(file.file.path)
            documents.delete()
            #insurance.delete()
            vehicle.delete()
        return redirect('vehicle:list')
    else:
        raise Http404

def vehicle_file_save(upload_file, vehicle, type):
    vehicle_file = VehicleDocument(
        vehicle_id=vehicle,
        file=upload_file,
        filename=upload_file.name,
        type=type
    )
    vehicle_file.save()
    # print(vehicle_file)
    return


def download(request, vehicle_id, file_id):
    download_file = get_object_or_404(VehicleDocument, pk=file_id)
    if download_file.vehicle_id == Vehicle.objects.get(pk=vehicle_id):
        url = download_file.vehicle_file.url
        root = str(BASE_DIR)+url

        if os.path.exists(root):
            with open(root, 'rb') as fh:
                quote_file_url = urllib.parse.quote(download_file.filename.encode('utf-8'))
                response = HttpResponse(fh.read(), content_type=mimetypes.guess_type(url)[0])
                response['Content-Disposition'] = 'attachment;filename*=UTF-8\'\'%s' % quote_file_url
                return response
            raise Http404
        else:
            #print("에러")
            raise Http404
    else:
        raise Http404


# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@

# class VehicleDetail(generic.DetailView):
#     template_name = 'vehicle/vehicle_detail.html'
#     context_object_name = 'vehicle'
#     model = Vehicle

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)

        
#         context['driver_list'] = Member.objects.filter(role="기사")
#         context['files'] = VehicleDocument.objects.filter(vehicle_id=self.kwargs['pk'])

#         return context

# def vehicle_create(request):
#     context = {}
#     if request.method == 'POST':
#         vehicle_form = VehicleDetailForm(request.POST)
#         insurance_form = VehicleInsuranceForm(request.POST)        
#         driver = get_object_or_404(Member, pk=request.POST.get('driver'))
        
#         if vehicle_form.is_valid():            
#             files = request.FILES.getlist('file', None)
#             print("aaaa", files)
#             vehicle = vehicle_form.save(commit=False)
#             vehicle.driver = driver
#             vehicle.save()
#             vehicle_file_save(files, vehicle)

#             return redirect('vehicle:vehicle_list')
#         else:
#             raise Http404

#     else:
#         context = {
#             'driver_list' : Member.objects.all(),            
#         }
#     return render(request, 'vehicle/vehicle_create.html', context)

# def vehicle_edit(request, pk):
#     vehicle = get_object_or_404(Vehicle, pk=pk)

#     if request.method == 'POST':
#         vehicle_form = VehicleDetailForm(request.POST)
#         #insurance_form = VehicleInsuranceForm(request.POST)
#         #if vehicle_form.is_valid() and insurance_form.is_valid():
#         if vehicle_form.is_valid():
#             files = request.FILES.getlist('file', None)
#             vehicle_file_save(files, vehicle)

#             post_driver = request.POST.get('driver')
#             if post_driver:
#                 vehicle.driver = get_object_or_404(Member, pk=post_driver)
#             vehicle.vehicle_num = vehicle_form.cleaned_data['vehicle_num']
#             vehicle.vehicle_id = vehicle_form.cleaned_data['vehicle_id']
#             vehicle.group = vehicle_form.cleaned_data['group']
#             vehicle.vehicle_type = vehicle_form.cleaned_data['vehicle_type']
#             vehicle.maker = vehicle_form.cleaned_data['maker']
#             vehicle.model_year = vehicle_form.cleaned_data['model_year']
#             vehicle.release_date = vehicle_form.cleaned_data['release_date']
#             vehicle.use = vehicle_form.cleaned_data['use']
#             vehicle.passenger_num = vehicle_form.cleaned_data['passenger_num']
            
#             vehicle.save()
#             #print("testetsetst", files)
#             return redirect('vehicle:vehicle_list')
#     raise Http404


# def vehicle_delete(request):
#     if request.method == 'POST':
#         pk_list = request.POST.getlist('check',None)
#         for pk in pk_list:
#             vehicle = get_object_or_404(Vehicle, pk=pk)
#             #insurance = get_object_or_404(VehicleInsurance, vehicle_id=pk)
#             #document = get_object_or_404(VehicleDocument, vehicle_id=pk)
#             document = VehicleDocument.objects.filter(vehicle_id=pk)
#             for files in document:
#                 os.remove(files.vehicle_file.path)
#             document.delete()
#             #insurance.delete()
#             vehicle.delete()
#         return redirect('vehicle:vehicle_list')
#     else:
#         raise Http404


# def vehicle_file_del(request, vehicle_id, file_id):
#     file = VehicleDocument.objects.get(pk=file_id)
#     os.remove(file.vehicle_file.path)
#     file.delete()
#     return redirect('vehicle:vehicle_detail', pk=vehicle_id)#여기서부터
#     #return render(request, 'vehicle/vehicle_detail.html', pk)
#     #return reverse('vehicle_detail', args=(vehicle_id))
    

# def vehicle_file_save(upload_file, vehicle):
#     for file in upload_file:
#         vehicle_file = VehicleDocument(
#             vehicle_id=vehicle,
#             vehicle_file=file,
#             filename=file.name,
#         )
#         vehicle_file.save()
#         print(vehicle_file)
#     return


# def download(request, vehicle_id, file_id):
#     download_file = get_object_or_404(VehicleDocument, pk=file_id)
#     if download_file.vehicle_id == Vehicle.objects.get(pk=vehicle_id):
#         url = download_file.vehicle_file.url
#         root = str(BASE_DIR)+url

#         if os.path.exists(root):
#             with open(root, 'rb') as fh:
#                 quote_file_url = urllib.parse.quote(download_file.filename.encode('utf-8'))
#                 response = HttpResponse(fh.read(), content_type=mimetypes.guess_type(url)[0])
#                 response['Content-Disposition'] = 'attachment;filename*=UTF-8\'\'%s' % quote_file_url
#                 return response
#             raise Http404
#         else:
#             #print("에러")
#             raise Http404
#     else:
#         raise Http404


#     '''def vehicle_edit(request):
#     if request.method == 'POST': # 폼이 제출되었을 경우...
#         form = ContactForm(request.POST) # 폼은 POST 데이터에 바인드됨
#         if form.is_valid(): # 모든 유효성 검증 규칙을 통과
#             # form.cleaned_data에 있는 데이터를 처리
#             # ...
#             return HttpResponseRedirect('../') # Redirect after POST
#     else:
#         form = ContactForm() # An unbound form

#     return render_to_response('contact.html', {
#         'form': form,
#     })'''

# '''
# class VehicleCreate(generic.edit.CreateView):
#     template_name = 'vehicle/vehicle_create.html'
#     model = Vehicle, Vehicle_insurance, Vehicle_document
#     fields = '__all__'

# class VehicleUpdate(generic.edit.UpdateView):
#     template_name = 'vehicle/vehicle_detail.html'
#     model = Vehicle, Vehicle_insurance, Vehicle_document
#     fields = '__all__'
# '''