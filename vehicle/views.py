import urllib
import os
import json
import mimetypes
from datetime import datetime
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q
from django.shortcuts import render, redirect, get_object_or_404
from django.http import Http404, JsonResponse, HttpResponse, HttpResponseNotAllowed
from django.views import generic
from django.urls import reverse
from config.settings import MEDIA_ROOT
import pandas as pd
from .models import Vehicle, VehicleDocument, Refueling, DailyChecklist, WeeklyChecklist, EquipmentChecklist
from .forms import VehicleForm
from humanresource.models import Member
from ERP.settings import BASE_DIR
from dateutil.relativedelta import relativedelta

TODAY = str(datetime.now())[:10]
FORMAT = "%Y-%m-%d"

def document_image(request, file_id):
    if request.session.get('authority') > 1:
        return render(request, 'authority.html')
    context = {
        'img': get_object_or_404(VehicleDocument, id=file_id)
    }
    return render(request, 'vehicle/document_img.html', context)

def efficiency(request):
    
    return render(request, 'vehicle/efficiency.html')

class MaintenanceList(generic.ListView):
    template_name = 'vehicle/maintenance.html'
    context_object_name = 'vehicle_list'
    model = Vehicle
    paginate_by = 10

# moved to humanresources app
# class AccidentList(generic.ListView):
#     template_name = 'vehicle/accident.html'
#     context_object_name = 'vehicle_list'
#     model = Vehicle
#     paginate_by = 10

class VehicleList(generic.ListView):
    template_name = 'vehicle/list.html'
    context_object_name = 'vehicle_list'
    model = Vehicle
    paginate_by = 10

    def get(self, request, *args, **kwargs):
        if request.session.get('authority') > 1:
            return render(request, 'authority.html')
        return super().get(request, *args, **kwargs)

    def get_queryset(self):
        select = self.request.GET.get('select', '')
        search = self.request.GET.get('search', '')
        use = self.request.GET.get('use', '사용')
        
        if select == 'vehicle' and search:
            vehicle = Vehicle.objects.filter(use=use).filter(vehicle_num__contains=search).order_by('vehicle_num0', 'vehicle_num')
        elif select == 'driver' and search:
            vehicle = Vehicle.objects.filter(use=use).filter(driver_name__contains=search).order_by('vehicle_num0', 'vehicle_num')
        elif select == 'passenger' and search:
            vehicle = Vehicle.objects.filter(use=use).filter(passenger_num__contains=search).order_by('vehicle_num0', 'vehicle_num')
        else:
            vehicle = Vehicle.objects.filter(use=use).order_by('vehicle_num0', 'vehicle_num')
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

        context['start_num'] = 1 + paginator.per_page * (current_page-1)

        context['select'] = self.request.GET.get('select', '')
        context['search'] = self.request.GET.get('search', '')
        context['use'] = self.request.GET.get('use', '사용')
        # context['driver_list'] = Member.objects.filter(role='운전원')
        context['driver_list'] = Member.objects.filter(vehicle=None).filter(Q(role='팀장') | Q(role='운전원') | Q(role='용역')).filter(use='사용').order_by('name')
        
        file_list = []
        for vehicle in context['vehicle_list']:
            files = VehicleDocument.objects.filter(vehicle_id=vehicle)
            list = []
            try:
                v_file = files.get(type="차량등록증")
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
    if request.session.get('authority') > 1:
        return render(request, 'authority.html')
    if request.method == 'POST':
        vehicle_form = VehicleForm(request.POST)
        if vehicle_form.is_valid():
            creator = get_object_or_404(Member, pk=request.session.get('user'))
            vehicle_registration_file = request.FILES.get('vehicle_registration', None)
            insurance_receipt_file = request.FILES.get('insurance_receipt', None)
            
            vehicle = vehicle_form.save(commit=False)
            if request.POST.get('driver'):
                driver = get_object_or_404(Member, pk=request.POST.get('driver'))
                vehicle.driver = driver
                vehicle.driver_name = driver.name
            vehicle.creator = creator
            vehicle.save()
            if vehicle_registration_file:
                vehicle_file_save(vehicle_registration_file, vehicle, "차량등록증", creator)

            if insurance_receipt_file:
                vehicle_file_save(insurance_receipt_file, vehicle, "insurance_receipt", creator)

            return redirect(request.META.get('HTTP_REFERER', 'redirect_if_referer_not_found'))
        else:
            raise Http404

    else:
        return HttpResponseNotAllowed(['post'])

def vehicle_edit(request):
    if request.session.get('authority') > 1:
        return render(request, 'authority.html')
    pk = request.POST.get('id', None)
    vehicle = get_object_or_404(Vehicle, pk=pk)

    if request.method == 'POST':
        vehicle_form = VehicleForm(request.POST)
        #insurance_form = VehicleInsuranceForm(request.POST)
        #if vehicle_form.is_valid() and insurance_form.is_valid():
        if vehicle_form.is_valid():
            if request.POST.get('driver', None):
                vehicle.driver = get_object_or_404(Member, id=request.POST.get('driver', None))
                vehicle.driver_name = vehicle.driver.name
            else:
                vehicle.driver = None
                vehicle.driver_name = ''
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
            vehicle.check_date = vehicle_form.cleaned_data['check_date']
            vehicle.type = vehicle_form.cleaned_data['type']
            vehicle.save()

            # 파일
            vehicle_file = request.FILES.get('vehicle_registration', None)
            v_file_name = request.POST.get('vehicle_registration_name', None)

            cur_files = VehicleDocument.objects.filter(vehicle_id=vehicle)
            try:
                cur_vehicle_files = cur_files.get(type='차량등록증')
            except:
                cur_vehicle_files = None

            if vehicle_file:
                if cur_vehicle_files:
                    os.remove(cur_vehicle_files.file.path)
                    cur_vehicle_files.delete()
                file = VehicleDocument(
                    vehicle_id=vehicle,
                    file=vehicle_file,
                    filename=vehicle_file.name,
                    type='차량등록증',
                )
                file.save()
            elif not v_file_name and cur_vehicle_files:
                os.remove(cur_vehicle_files.file.path)
                cur_vehicle_files.delete()

                
            return redirect(request.META.get('HTTP_REFERER', 'redirect_if_referer_not_found'))
        else:
            Http404
    raise Http404


def vehicle_delete(request):
    if request.session.get('authority') > 1:
        return render(request, 'authority.html')
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
        return redirect(request.META.get('HTTP_REFERER', 'redirect_if_referer_not_found'))
    else:
        raise Http404

def vehicle_download(request):
    if request.session.get('authority') > 1:
        return render(request, 'authority.html')
    datalist = list(Vehicle.objects.exclude(use='삭제').order_by('vehicle_num0', 'vehicle_num').values_list( 'id', 'vehicle_num0', 'vehicle_num', 'vehicle_id', 'motor_type', 'rated_output', 'vehicle_type', 'maker', 'model_year', 'release_date', 'driver', 'driver_name', 'use', 'passenger_num', 'check_date', 'type'))
    
    try:
        df = pd.DataFrame(datalist, columns=['id', '차량번호 앞자리', '차량번호', '차대번호', '원동기형식', '정격출력', '차량이름', '제조사', '연식', '출고일자', '담당기사id', '담당기사', '사용여부', '승차인원', '정기점검일', '형식'])
        url = f'{MEDIA_ROOT}/vehicle/vehicleDataList.xlsx'
        df.to_excel(url, index=False)

        if os.path.exists(url):
            with open(url, 'rb') as fh:
                quote_file_url = urllib.parse.quote('차량목록.xlsx'.encode('utf-8'))
                response = HttpResponse(fh.read(), content_type=mimetypes.guess_type(url)[0])
                response['Content-Disposition'] = 'attachment;filename*=UTF-8\'\'%s' % quote_file_url
                return response
    except Exception as e:
        print(e)
        #return JsonResponse({'status': 'fail', 'e': e})
        raise Http404

def vehicle_file_download(request):
    if request.session.get('authority') > 1:
        return render(request, 'authority.html')

def vehicle_upload(request):
    if request.session.get('authority') > 1:
        return render(request, 'authority.html')
    creator = get_object_or_404(Member, pk=request.session['user'])
    post_data = json.loads(request.body)
    
    count = 0
    for data in post_data:
        count += 1
        try:
            if data['id']:
                Vehicle.objects.get(id=data['id'])
            if data['driver']:
                driver = Member.objects.get(id=data['driver'])
                if driver.name != data['driver_name']:
                    # 기사 이름 안 맞음
                    return JsonResponse({'error': 'driver_name', 'status': 'fail', 'count': count})
                if Vehicle.objects.filter(driver=driver).exists():
                    # 담당 기사는 차량 1대에 1명씩
                    return JsonResponse({'error': 'driver_overlap', 'status': 'fail', 'count': count})
        except Vehicle.DoesNotExist:
            # 차량 id 안 맞음
            return JsonResponse({'error': 'vehicle_id', 'status': 'fail', 'count': count})
        except Member.DoesNotExist:
            # 기사 id 안 맞음
            return JsonResponse({'error': 'driver_id', 'status': 'fail', 'count': count})
        
        if not data['vehicle_num0'] or not data['vehicle_num']:
            # 차량번호 없음
            return JsonResponse({'error': 'vehicle_num', 'status': 'fail', 'count': count})
    
    count = 0
    try:
        for data in post_data:
            count += 1
            driver = Member.objects.get(id=data['driver']) if data['driver'] else ''
            if data['id']:
                vehicle = Vehicle.objects.get(id=data['id'])
                vehicle.vehicle_num0 = data['vehicle_num0']
                vehicle.vehicle_num = data['vehicle_num']
                vehicle.vehicle_id = data['vehicle_id']
                vehicle.motor_type = data['motor_type']
                vehicle.rated_output = data['rated_output']
                vehicle.vehicle_type = data['vehicle_type']
                vehicle.maker = data['maker']
                vehicle.model_year = data['model_year']
                vehicle.release_date = data['release_date']
                vehicle.driver_name = data['driver_name']
                vehicle.use = data['use']
                vehicle.passenger_num = data['passenger_num']
                vehicle.check_date = data['check_date']
                vehicle.type = data['type']
            else:
                vehicle = Vehicle(
                    vehicle_num0 = data['vehicle_num0'],
                    vehicle_num = data['vehicle_num'],
                    vehicle_id = data['vehicle_id'],
                    motor_type = data['motor_type'],
                    rated_output = data['rated_output'],
                    vehicle_type = data['vehicle_type'],
                    maker = data['maker'],
                    model_year = data['model_year'],
                    release_date = data['release_date'],
                    driver_name = data['driver_name'],
                    use = data['use'],
                    passenger_num = data['passenger_num'],
                    check_date = data['check_date'],
                    type = data['type'],
                    creator = creator
                )
            if driver:
                vehicle.driver = driver
            vehicle.save()
    except Exception as e:
        # 데이터 생성 중 에러발생
        return JsonResponse({'status' : 'fail', 'error' : str(e), 'count': count})
    return JsonResponse({'status': 'success', 'count': count})

def vehicle_file_save(upload_file, vehicle, type, creator):
    vehicle_file = VehicleDocument(
        vehicle_id=vehicle,
        file=upload_file,
        filename=upload_file.name,
        type=type,
        creator=creator,
    )
    vehicle_file.save()
    return


def download(request, vehicle_id, file_id):
    if request.session.get('authority') > 1:
        return render(request, 'authority.html')
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
            raise Http404
    else:
        raise Http404

class RefuelingList(generic.ListView):
    template_name = 'vehicle/refueling.html'
    context_object_name = 'refueling_list'
    model = Refueling
    paginate_by = 10

    def get(self, request, *args, **kwargs):
        if request.session.get('authority') > 1:
            return render(request, 'authority.html')
        return super().get(request, *args, **kwargs)

    def get_queryset(self):
        select = self.request.GET.get('select', '')
        search = self.request.GET.get('search', '')
        
        if select == 'vehicle' and search:
            vehicle = Refueling.objects.filter(vehicle__vehicle_num__contains=search).order_by('refueling_date')
        elif select == 'driver' and search:
            vehicle = Refueling.objects.filter(driver_driver_name__contains=search).order_by('refueling_date')
        else:
            vehicle = Refueling.objects.order_by('refueling_date')
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

        context['start_num'] = 1 + paginator.per_page * (current_page-1)
        context['select'] = self.request.GET.get('select', '')
        context['search'] = self.request.GET.get('search', '')

        return context

def refueling_delete(request):
    if request.session.get('authority') > 1:
        return render(request, 'authority.html')
    if request.method == 'POST':
        pk_list = request.POST.getlist('check',None)
        for pk in pk_list:
            refueling = get_object_or_404(Refueling, pk=pk)
            
            refueling.delete()
        return redirect(request.META.get('HTTP_REFERER', 'redirect_if_referer_not_found'))
    else:
        return HttpResponseNotAllowed(['post'])



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
        context['insurance_list'] = context['vehicle_list'].exclude(insurance_expiry_date='').filter(insurance_expiry_date__lte=i_next_month).order_by('insurance_expiry_date')

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
        
        context['check_list'] = context['vehicle_list'].exclude(check_duration='').filter(check_duration__lte=c_next_month).order_by('check_duration')
        
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


def insurance_edit(request):
    if request.method == 'POST':
        id = request.POST.get('id')
        vehicle = get_object_or_404(Vehicle, id=id)

        date = request.POST.get('date')
        if date:
            vehicle.insurance_expiry_date = date
            vehicle.save()
        
        insurance_file = request.FILES.get('insurance_receipt', None)
        i_file_name = request.POST.get('insurance_receipt_name', None)
        cur_files = VehicleDocument.objects.filter(vehicle_id=vehicle)
        try:
            cur_insurance_files = cur_files.get(type='insurance_receipt')
        except:
            cur_insurance_files = None

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


        return redirect(request.META.get('HTTP_REFERER', 'redirect_if_referer_not_found'))

    return HttpResponseNotAllowed(['post'])



def check_edit(request):
    if request.method == 'POST':
        id = request.POST.get('id')
        vehicle = get_object_or_404(Vehicle, id=id)

        date = request.POST.get('date')
        if date:
            vehicle.check_duration = date
            vehicle.save()
    


        return redirect(request.META.get('HTTP_REFERER', 'redirect_if_referer_not_found'))

    return HttpResponseNotAllowed(['post'])


class DailyChecklistListView(generic.ListView):
    template_name = 'vehicle/dailychecklist.html'
    context_object_name = 'dailychecklist_list'
    model = DailyChecklist

    def get_queryset(self):
        # select = self.request.GET.get('select', '')
        name = self.request.GET.get('name', '')
        date = self.request.GET.get('date', TODAY)
        # use = self.request.GET.get('use', '사용')
        
        # dailychecklist = DailyChecklist.objects.filter(date__contains=date)
        if date == '' : date = TODAY

        if name:
            # dailychecklist = dailychecklist.daily_checklist_bus_id.objects.filter(vehicle_num__contains=search).order_by('vehicle_num0', 'vehicle_num')
            dailychecklist = DailyChecklist.objects.filter(member__name__contains=name).filter(date__contains=date).order_by('member', 'bus_id__vehicle_num0', 'bus_id__vehicle_num')
        else:
            # dailychecklist = dailychecklist.daily_checklist_bus_id.objects.order_by('vehicle_num0', 'vehicle_num')
            dailychecklist = DailyChecklist.objects.filter(date__contains=date).order_by('member', 'bus_id__vehicle_num0', 'bus_id__vehicle_num')
        return dailychecklist


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['name'] = self.request.GET.get('name', '')
        context['date'] = self.request.GET.get('date', TODAY)
        
        return context


class WeeklyChecklistListView(generic.ListView):
    template_name = 'vehicle/weeklychecklist.html'
    context_object_name = 'weeklychecklist_list'
    model = WeeklyChecklist

    def get_queryset(self):
        name = self.request.GET.get('name', '')
        date = self.request.GET.get('date', TODAY)
        if date == '' : date = TODAY

        if name:
            weeklychecklist = WeeklyChecklist.objects.filter(member__name__contains=name).filter(date__contains=date).order_by('member', 'bus_id__vehicle_num0', 'bus_id__vehicle_num')
        else:
            weeklychecklist = WeeklyChecklist.objects.filter(date__contains=date).order_by('member', 'bus_id__vehicle_num0', 'bus_id__vehicle_num')
        return weeklychecklist


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['name'] = self.request.GET.get('name', '')
        context['date'] = self.request.GET.get('date', TODAY)
        
        return context


class EquipmentChecklistListView(generic.ListView):
    template_name = 'vehicle/equipmentchecklist.html'
    context_object_name = 'equipmentchecklist_list'
    model = EquipmentChecklist

    def get_queryset(self):
        name = self.request.GET.get('name', '')
        date = self.request.GET.get('date', TODAY)
        if date == '' : date = TODAY

        if name:
            equipmentchecklist = EquipmentChecklist.objects.filter(member__name__contains=name).filter(date__contains=date).order_by('member', 'bus_id__vehicle_num0', 'bus_id__vehicle_num')
        else:
            equipmentchecklist = EquipmentChecklist.objects.filter(date__contains=date).order_by('member', 'bus_id__vehicle_num0', 'bus_id__vehicle_num')
        return equipmentchecklist


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['name'] = self.request.GET.get('name', '')
        context['date'] = self.request.GET.get('date', TODAY)
        
        return context

class  MaintenanceGraph(generic.ListView):
    template_name = 'vehicle/maintenancegraph.html'
    context_object_name = 'member_list'
    model = Member
    authority_level = 3

    def get(self, request, *args, **kwargs):
        members = self.model.objects.all()
        context = {
            self.context_object_name: members
        }
        return render(request, self.template_name, context)

class  InspectionLog(generic.ListView):
    template_name = 'vehicle/inspectionlog.html'
    context_object_name = 'member_list'
    model = Member
    authority_level = 3

    def get(self, request, *args, **kwargs):
        members = self.model.objects.all()
        context = {
            self.context_object_name: members
        }
        return render(request, self.template_name, context)

class  PartsManagement(generic.ListView):
    template_name = 'vehicle/partsmanagement.html'
    context_object_name = 'member_list'
    model = Member
    authority_level = 3

    def get(self, request, *args, **kwargs):
        members = self.model.objects.all()
        context = {
            self.context_object_name: members
        }
        return render(request, self.template_name, context)