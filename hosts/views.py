from django.shortcuts import render
from .forms import UploadFileForm, ComPerCityForm
from .models import Commission
from django.views.generic import ListView
from django.db.models import Sum
from django.contrib import messages
import csv, io



class ListCommisionsAllView(ListView):
    model = Commission
    template_name = 'hosts/list-commisions.html'
    context_object_name = 'commisions'

    def post(self,request,*args, **kwarg):
        Commission.objects.all().delete()
        return render(request, 'hosts/list-commisions.html')
        

class ListCommisionsMonthView(ListView):
    model = Commission
    template_name = 'hosts/commission-per-month.html'
    context_object_name = 'commisions'

    def get_queryset(self,*args, **kwargs):
        queryset = super().get_queryset()
        year=set() #take unique years from dataset
        for y in queryset:
            year.add(y.checkin_year) #add year to year set
        lst = ['January','February','March','April',
                'May','June','July','August','September',
                'October','November','December']
        queryset={}
        for i in lst: #iterate trough list of months 
            for z in year: #for every year check every month
                queryset[i+"/"+z] = Commission.objects.filter(checkin_month__contains = i).filter(checkin_year__contains = z).aggregate(Sum('income'))['income__sum']
        for k,v in list(queryset.items()): #take off None values
            if v == None:
                del queryset[k]    
        return queryset


def com_per_city(request):
    form  = ComPerCityForm()
    if request.method == 'POST':
        form = ComPerCityForm(request.POST)
        if form.is_valid():
            city = form.cleaned_data['city']
            if city == "LONDON": #set commission percent per specific city
                data = Commission.objects.filter(city = city).aggregate(Sum('income'))['income__sum']*0.10
            elif city == "PARIS": #set commission percent per specific city
                data = Commission.objects.filter(city = city).aggregate(Sum('income'))['income__sum']*0.12
            elif city == "PORTO": #set commission percent per specific city
                data = Commission.objects.filter(city = city).aggregate(Sum('income'))['income__sum']*0.09
            return render(request, 'hosts/commission-per-city.html', {'form': form,'data': data, 'city':city})
    return render(request, 'hosts/commission-per-city.html', {'form': form})


def upload_view(request):
    form = UploadFileForm()
    message = ''
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            message = "Uploaded Successfully!"
            csv_file = request.FILES['select_file'] #get uploaded file
            data_set = csv_file.read().decode('UTF-8')
            io_string  = io.StringIO(data_set)
            next(io_string) #exclude first row   
            for element in csv.reader(io_string, delimiter = ',' ):
                reservation = element[0] #get reservation from dataset
                year, month, day = element[1].split("-") #split checkind date in year,month,day 
                checkin_year, checkin_month, checkin_day = year, month, day
                checkout = element[2]#get checkout from dataset
                flat = element[3]#get flat from dataset
                city = element[4]#get city from dataset
                income = element[5]#get income from dataset
                Commission.objects.create(reservation = reservation, #creare new object in db
                    checkin_month=checkin_month, checkin_year=checkin_year, checkin_day=checkin_day,
                    checkout = checkout,flat=flat, city=city, income=float(income))
    else:
        form = UploadFileForm()
    return render(request, 'hosts/load_form.html', {'form':form , 'message':message})
