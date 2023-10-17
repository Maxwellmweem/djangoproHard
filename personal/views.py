from django.shortcuts import render 
from account.models import Account

def home_screen_view(request):
	
    context = {} 
    

    account = Account.objects.all()
    context['accounts'] = account

    return render(request, "personal/home.html",context) 

def about_view(request):
    return render(request, 'personal/about.html')

def services_view(request):
    return render(request, 'personal/services.html')



