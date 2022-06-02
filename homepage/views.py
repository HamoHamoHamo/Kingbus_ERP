from django.shortcuts import render, redirect


def home(request):
    return render(request, 'homepage/home.html')

def trp(request):
    return render(request, 'homepage/trp.html')

def dispatch(request):
    return render(request, 'homepage/dispatch.html')

def servicelink(request):
    return render(request, 'homepage/servicelink.html')
    
def web(request):
    return render(request, 'homepage/web.html')
    
def customizing(request):
    return render(request, 'homepage/customizing.html')
    
def kingbus(request):
    return render(request, 'homepage/kingbus.html')
    
def driver(request):
    return render(request, 'homepage/driver.html')
    
def check(request):
    return render(request, 'homepage/check.html')
    
def consulting(request):
    return render(request, 'homepage/consulting.html')
    
def payment(request):
    return render(request, 'homepage/payment.html')
    
