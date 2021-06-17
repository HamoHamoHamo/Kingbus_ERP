import urllib
import os
import mimetypes
from django.shortcuts import render, redirect, get_object_or_404
from django.http import Http404, HttpResponse
from django.views import generic
from django.urls import reverse
from .models import Vehicle, VehicleDocument, VehicleInsurance, VehicleCheck
from .forms import VehicleDetailForm, VehicleInsuranceForm, VehicleDocumentForm
from ERP.settings import BASE_DIR

# Create your views here.
'''def home(request):
    return render(request, 'vehicle/home.html')'''

class VehicleList(generic.ListView):
    template_name = 'vehicle/vehicle_list.html'
    context_object_name = 'vehicle'
    model = Vehicle


def vehicle_detail(request, pk):
    context = {}
    vehicle = get_object_or_404(Vehicle, pk=pk)
    insurance = get_object_or_404(VehicleInsurance, vehicle_id=pk)
    if request.method == 'POST':
        vehicle_form = VehicleDetailForm(request.POST, instance=vehicle)
        insurance_form = VehicleInsuranceForm(request.POST, instance=insurance)
        if vehicle_form.is_valid() and insurance_form.is_valid():
            files = request.FILES.getlist('file', None)
            vehicle_file_save(files, vehicle)
            vehicle_form.save()
            insurance_form.vehicle_id = vehicle
            insurance_form.save()
            #print("testetsetst", files)
        return redirect('vehicle:vehicle_list')
    if request.method == 'GET':
        vehicle_ins = Vehicle.objects.get(pk=pk)
        insurance_ins = VehicleInsurance.objects.get(vehicle_id=pk)
        try:
            vehicle_file_ins = VehicleDocument.objects.get(vehicle_id=pk)
            vehicle_file_form = VehicleDocumentForm(instance=vehicle_file_ins)
        except:
            vehicle_file_ins = ""
            vehicle_file_form = ""
        vehicle_form = VehicleDetailForm(instance=vehicle_ins)
        insurance_form = VehicleInsuranceForm(instance=insurance_ins)
        context = {
            'vehicle_form': vehicle_form,
            'insurance_form': insurance_form,
            'file_form': vehicle_file_form,
            'vehicle': vehicle_ins,
            'file': VehicleDocument.objects.filter(vehicle_id=pk),
        }
    else:
        context = {
            'vehicle_form' : VehicleDetailForm(),
            'insurance_form' : VehicleInsuranceForm(),
        }
    return render(request, 'vehicle/vehicle_detail.html', context)

    #create 완료~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def vehicle_create(request):
    context = {}
    if request.method == 'POST':
        vehicle_form = VehicleDetailForm(request.POST)
        insurance_form = VehicleInsuranceForm(request.POST)
        if vehicle_form.is_valid() and insurance_form.is_valid():
            files = request.FILES.getlist('file', None)
            vehicle = vehicle_form.save(commit=True)
            insurance = insurance_form.save(commit=False)
            insurance.vehicle_id = vehicle
            insurance.save()
            vehicle_file_save(files, vehicle)
            return redirect('vehicle:vehicle_list')
    else:
        context = {
            'vehicle_form' : VehicleDetailForm(),
            'insurance_form' : VehicleInsuranceForm(),
        }
    return render(request, 'vehicle/vehicle_create.html', context)


def vehicle_delete(request, pk):
    if request.method == 'POST':
        vehicle = get_object_or_404(Vehicle, pk=pk)
        insurance = get_object_or_404(VehicleInsurance, vehicle_id=pk)
        #document = get_object_or_404(VehicleDocument, vehicle_id=pk)
        document = VehicleDocument.objects.filter(vehicle_id=pk)
        for files in document:
            os.remove(files.vehicle_file.path)
        document.delete()
        insurance.delete()
        vehicle.delete()
        return redirect('vehicle:vehicle_list')
    else:
        return render(request, 'vehicle/vehicle_delete.html')


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