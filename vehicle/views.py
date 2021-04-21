from django.shortcuts import render, redirect, get_object_or_404
from django.views import generic
from .models import Vehicle, VehicleDocument, VehicleInsurance, VehicleCheck
from .forms import VehicleDetailForm, VehicleInsuranceForm

# Create your views here.
'''def home(request):
    return render(request, 'vehicle/home.html')'''

class VehicleList(generic.ListView):
    template_name = 'vehicle/vehicle_list.html'
    context_object_name = 'vehicle'
    model = Vehicle

class VehicleDetail(generic.UpdateView):
    template_name = 'vehicle/vehicle_detail.html'
    context_object_name = 'vehicle'
    model = Vehicle
    fields = '__all__'

    
    
    
def vehicle_create(request):
    context = {}
    if request.method == 'POST':
        vehicle_form = VehicleDetailForm(request.POST)
        insurance_form = VehicleInsuranceForm(request.POST)
        if vehicle_form.is_valid() and insurance_form.is_valid():
            vehicle = vehicle_form.save(commit=True)
            insurance = insurance_form.save(commit=False)
            insurance.vehicle_id = vehicle
            insurance.save()           
            return redirect('vehicle:vehicle_list')
    else:
        context = {
            'vehicle_form' : VehicleDetailForm(),
            'insurance_form' : VehicleInsuranceForm(),
        }
    return render(request, 'vehicle/vehicle_create.html', context)









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