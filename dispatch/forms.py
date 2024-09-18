from django import forms 
import re

from .models import DispatchOrder, DispatchOrderConnect, DispatchRegularlyData, Station, DispatchRegularly, DispatchOrderTour, DispatchOrderTourCustomer

class RegularlyDataForm(forms.ModelForm):
    departure_time1 = forms.CharField(max_length=2, required=True)
    departure_time2 = forms.CharField(max_length=2, required=True)
    arrival_time1 = forms.CharField(max_length=2, required=True)
    arrival_time2 = forms.CharField(max_length=2, required=True)


    class Meta:
        model = DispatchRegularlyData
        fields = [
            'references',
            'departure',
            'arrival',
            'number1',
            'number2',
            'work_type',
            'route',
            'location',
            'detailed_route',
            'maplink',
            'use',

            # clean에서 따로 처리
            'price',
            'driver_allowance',
            'driver_allowance2',
            'outsourcing_allowance',
            'departure_time1',
            'departure_time2',
            'arrival_time1',
            'arrival_time2',
            'week',
        ]

    def clean(self):
        cleaned_data = super().clean()
        
        # 시간 처리
        departure_time1 = cleaned_data.get('departure_time1')
        departure_time2 = cleaned_data.get('departure_time2')
        arrival_time1 = cleaned_data.get('arrival_time1')
        arrival_time2 = cleaned_data.get('arrival_time2')

        if len(departure_time1) < 2:
            departure_time1 = f'0{departure_time1}'
        if len(departure_time2) < 2:
            departure_time2 = f'0{departure_time2}'
        if len(arrival_time1) < 2:
            arrival_time1 = f'0{arrival_time1}'
        if len(arrival_time2) < 2:
            arrival_time2 = f'0{arrival_time2}'

        departure_time = f'{departure_time1}:{departure_time2}'
        arrival_time = f'{arrival_time1}:{arrival_time2}'

        if arrival_time < departure_time:
            raise forms.ValidationError('출발시간이 도착시간보다 늦습니다.')

        cleaned_data['departure_time'] = departure_time
        cleaned_data['arrival_time'] = arrival_time

        # 가격 처리
        price = cleaned_data.get('price')
        driver_allowance = cleaned_data.get('driver_allowance')
        driver_allowance2 = cleaned_data.get('driver_allowance2')
        outsourcing_allowance = cleaned_data.get('outsourcing_allowance')

        cleaned_data['price'] = int(price.replace(',', '')) if price else 0
        cleaned_data['driver_allowance'] = int(driver_allowance.replace(',', '')) if driver_allowance else 0
        cleaned_data['driver_allowance2'] = int(driver_allowance2.replace(',', '')) if driver_allowance2 else 0
        cleaned_data['outsourcing_allowance'] = int(outsourcing_allowance.replace(',', '')) if outsourcing_allowance else 0

        return cleaned_data

    def save(self, commit=True):
        instance = super().save(commit=False)
        cleaned_data = self.cleaned_data

        instance.num1 = re.sub(r'[^0-9]', '', instance.number1)
        instance.num2 = re.sub(r'[^0-9]', '', instance.number2)
        instance.price = cleaned_data['price']
        instance.driver_allowance = cleaned_data['driver_allowance']
        instance.driver_allowance2 = cleaned_data['driver_allowance2']
        instance.outsourcing_allowance = cleaned_data['outsourcing_allowance']
        instance.departure_time = cleaned_data['departure_time']
        instance.arrival_time = cleaned_data['arrival_time']
        instance.week = ' '.join(self.data.getlist('week', ''))

        if commit:
            instance.save()
        return instance

class RegularlyForm(RegularlyDataForm):
    class Meta(RegularlyDataForm.Meta):
        model = DispatchRegularly

class OrderForm(forms.ModelForm):
    class Meta:
        model = DispatchOrder
        fields = [
            'operation_type',
            'references',
            'departure',
            'arrival',
            'bus_type',
            'bus_cnt',
            'contract_status',
            'customer',
            'customer_phone',
            'bill_place',
            'ticketing_info',
            'order_type',
            'operating_company',
            'reservation_company',
            'driver_lease',
            'vehicle_lease',
            'time',
        ]
        
        # widgets = {
        #     'departure_date': forms.DateInput(format='%Y-%m-%d H:i', attrs={'type':'datetime-local'}),
        #     'arrival_date': forms.DateInput(format='%Y-%m-%d H:i', attrs={'type':'datetime-local'}),
        # }
        

class ConnectForm(forms.ModelForm):
    class Meta:
        model = DispatchOrderConnect
        fields = [
            'bus_id',
            'driver_id',
            'departure_date',
            'arrival_date',
        ]

class StationForm(forms.ModelForm):
    class Meta:
        model = Station
        fields = [
            'name',
            'address',
            'latitude',
            'longitude',
            'references',
        ]

class TourForm(forms.ModelForm):
    class Meta:
        model = DispatchOrderTour
        fields = [
            'firebase_uid',
            'price',
            'max_people',
        ]