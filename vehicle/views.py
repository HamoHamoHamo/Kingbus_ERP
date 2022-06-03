import urllib
import os
import mimetypes
from django.shortcuts import render, redirect, get_object_or_404
from django.http import Http404, HttpResponse
from django.views import generic
from django.urls import reverse
from .models import Vehicle, VehicleDocument, VehicleInsurance, VehicleCheck
from .forms import VehicleDetailForm, VehicleInsuranceForm, VehicleDocumentForm
from humanresource.models import Member
from ERP.settings import BASE_DIR

def list(request):

    return render(request, 'vehicle/list.html')

def mgmt(request):

    return render(request, 'vehicle/mgmt.html')


class VehicleList(generic.ListView):
    template_name = 'vehicle/vehicle_list.html'
    context_object_name = 'vehicle'
    model = Vehicle

    def get_queryset(self):
        vehicle_num = self.request.GET.get('vehicle_num', None)
        driver_name = self.request.GET.get('driver_name', None)
        
        if not vehicle_num and not driver_name:
            vehicle = Vehicle.objects.all()
        else:
            vehicle = None
            if driver_name:
                driver_list = Member.objects.filter(role="기사", name__contains=driver_name)
                
                for driver in driver_list:
                    if not vehicle:
                        vehicle = Vehicle.objects.filter(driver=driver)
                        print(vehicle,"a")
                    vehicle = vehicle | vehicle.filter(driver=driver)
                    print(vehicle,"aa")
            if vehicle_num:
                if vehicle:
                    vehicle = vehicle.filter(vehicle_num__contains=vehicle_num)               
                elif not driver_name:
                    vehicle = Vehicle.objects.filter(vehicle_num__contains=vehicle_num)
                
        return vehicle


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        return context


class VehicleDetail(generic.DetailView):
    template_name = 'vehicle/vehicle_detail.html'
    context_object_name = 'vehicle'
    model = Vehicle

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        
        context['driver_list'] = Member.objects.filter(role="기사")
        context['files'] = VehicleDocument.objects.filter(vehicle_id=self.kwargs['pk'])

        return context

def vehicle_create(request):
    context = {}
    if request.method == 'POST':
        vehicle_form = VehicleDetailForm(request.POST)
        insurance_form = VehicleInsuranceForm(request.POST)        
        driver = get_object_or_404(Member, pk=request.POST.get('driver'))
        
        if vehicle_form.is_valid():            
            files = request.FILES.getlist('file', None)
            print("aaaa", files)
            vehicle = vehicle_form.save(commit=False)
            vehicle.driver = driver
            vehicle.save()
            vehicle_file_save(files, vehicle)

            return redirect('vehicle:vehicle_list')
        else:
            raise Http404

    else:
        context = {
            'driver_list' : Member.objects.all(),            
        }
    return render(request, 'vehicle/vehicle_create.html', context)

def vehicle_edit(request, pk):
    vehicle = get_object_or_404(Vehicle, pk=pk)

    if request.method == 'POST':
        vehicle_form = VehicleDetailForm(request.POST)
        #insurance_form = VehicleInsuranceForm(request.POST)
        #if vehicle_form.is_valid() and insurance_form.is_valid():
        if vehicle_form.is_valid():
            files = request.FILES.getlist('file', None)
            vehicle_file_save(files, vehicle)

            post_driver = request.POST.get('driver')
            if post_driver:
                vehicle.driver = get_object_or_404(Member, pk=post_driver)
            vehicle.vehicle_num = vehicle_form.cleaned_data['vehicle_num']
            vehicle.vehicle_id = vehicle_form.cleaned_data['vehicle_id']
            vehicle.group = vehicle_form.cleaned_data['group']
            vehicle.vehicle_type = vehicle_form.cleaned_data['vehicle_type']
            vehicle.maker = vehicle_form.cleaned_data['maker']
            vehicle.model_year = vehicle_form.cleaned_data['model_year']
            vehicle.release_date = vehicle_form.cleaned_data['release_date']
            vehicle.use = vehicle_form.cleaned_data['use']
            vehicle.passenger_num = vehicle_form.cleaned_data['passenger_num']
            
            vehicle.save()
            #print("testetsetst", files)
            return redirect('vehicle:vehicle_list')
    raise Http404


def vehicle_delete(request):
    if request.method == 'POST':
        pk_list = request.POST.getlist('check',None)
        for pk in pk_list:
            vehicle = get_object_or_404(Vehicle, pk=pk)
            #insurance = get_object_or_404(VehicleInsurance, vehicle_id=pk)
            #document = get_object_or_404(VehicleDocument, vehicle_id=pk)
            document = VehicleDocument.objects.filter(vehicle_id=pk)
            for files in document:
                os.remove(files.vehicle_file.path)
            document.delete()
            #insurance.delete()
            vehicle.delete()
        return redirect('vehicle:vehicle_list')
    else:
        raise Http404


def vehicle_file_del(request, vehicle_id, file_id):
    file = VehicleDocument.objects.get(pk=file_id)
    os.remove(file.vehicle_file.path)
    file.delete()
    return redirect('vehicle:vehicle_detail', pk=vehicle_id)#여기서부터
    #return render(request, 'vehicle/vehicle_detail.html', pk)
    #return reverse('vehicle_detail', args=(vehicle_id))
    

def vehicle_file_save(upload_file, vehicle):
    for file in upload_file:
        vehicle_file = VehicleDocument(
            vehicle_id=vehicle,
            vehicle_file=file,
            filename=file.name,
        )
        vehicle_file.save()
        print(vehicle_file)
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


    '''def vehicle_edit(request):
    if request.method == 'POST': # 폼이 제출되었을 경우...
        form = ContactForm(request.POST) # 폼은 POST 데이터에 바인드됨
        if form.is_valid(): # 모든 유효성 검증 규칙을 통과
            # form.cleaned_data에 있는 데이터를 처리
            # ...
            return HttpResponseRedirect('../') # Redirect after POST
    else:
        form = ContactForm() # An unbound form

    return render_to_response('contact.html', {
        'form': form,
    })'''

'''
class VehicleCreate(generic.edit.CreateView):
    template_name = 'vehicle/vehicle_create.html'
    model = Vehicle, Vehicle_insurance, Vehicle_document
    fields = '__all__'

class VehicleUpdate(generic.edit.UpdateView):
    template_name = 'vehicle/vehicle_detail.html'
    model = Vehicle, Vehicle_insurance, Vehicle_document
    fields = '__all__'
'''