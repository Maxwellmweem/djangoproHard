from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from .models import Member,BiometricData,Account 
from django.urls import reverse
from .forms import BiometricDataForm
from django.contrib.auth.decorators import login_required
from django.core.files.storage import FileSystemStorage 
from account.models import Account
from django.http import HttpResponseServerError,HttpResponse, HttpResponseBadRequest
import logging
from django.contrib import messages
from django.utils.html import format_html
from django.core.files.base import ContentFile
import mimetypes

from account.forms import RegistrationForm, AccountAuthenticationForm, AccountUpdateForm,MemberForm

import base64
import mimetypes
from django.http import JsonResponse
from rest_framework import generics
from .models import BiometricData
from .serializers import BiometricDataSerializer
from django.views.decorators.csrf import csrf_protect





def registration_view(request):
    context = {}

    if  request.POST:
        registration_form = RegistrationForm(request.POST)
        
        if  registration_form.is_valid():
            account = registration_form.save()
            email = registration_form.cleaned_data.get('email')
            raw_password = registration_form.cleaned_data.get('password1')
            account = authenticate(email=email, password=raw_password)
            login(request, account)


            return redirect('member')
        else:
            context['registration_form'] = registration_form
    else:
        registration_form = RegistrationForm()
        context['registration_form'] = registration_form

    return render(request, 'account/register.html', context)

def member_view(request):
    context = {}

    if request.method == 'POST':
        member_form = MemberForm(request.POST)
        if member_form.is_valid():
            # Create a new Member instance and associate it with the logged-in user
            member_info = member_form.save(commit=False)
            member_info.account = request.user
            member_info.save()
            print("Member saved successfully!")  # Add this line for debugging
            return redirect('biometric_access_control')  # Redirect to the home page or any other desired page
        else:
            print("Form errors:", member_form.errors)  # Add this line for debugging
    else:
        member_form = MemberForm()

    context['member_form'] = member_form
    return render(request, 'account/MembershipForm.html', context)



class BiometricDataListCreateView(generics.ListCreateAPIView):
    queryset = BiometricData.objects.all()
    serializer_class = BiometricDataSerializer




def biometric_access_control_view(request):
    # Your view logic here
    return render(request, 'account/biometric_access_control.html')



def home_view(request):
    # Logic for handling form submissions (if applicable)
    if request.method == 'POST':
        form = YourForm(request.POST)
        if form.is_valid():
            # Process the form data and save it to the database
            instance = form.save()
            # Redirect back to the home page or any other page
            return redirect('home')  # Change 'home' to your actual URL name

    # Logic for rendering the home page
    context = {
        # Add any context data you need for rendering the template
    }
    return render(request, 'home.html', context)	

def logout_view(request):
	logout(request)
	return redirect('home')



def login_view(request):

	context = {}

	user = request.user
	if user.is_superuser: 
		return redirect("admin:index")	

	if request.POST:
		form = AccountAuthenticationForm(request.POST)
		if form.is_valid():
			email = request.POST['email']
			password = request.POST['password']
			user = authenticate(email=email, password=password)

			if user:
				login(request, user)
				return redirect("biometric_access_control")

	else:
		form = AccountAuthenticationForm()

	context['login_form'] = form

	# print(form)
	return render(request, "account/login.html", context)


def account_view(request):

	if not request.user.is_authenticated:
			return redirect("login")

	context = {}
	if request.POST:
		form = AccountUpdateForm(request.POST, instance=request.user)
		if form.is_valid():
			form.initial = {
					"email": request.POST['email'],
					"username": request.POST['username'],
			}
			form.save()
			context['success_message'] = "Updated"
	else:
		form = AccountUpdateForm(

			initial={
					"email": request.user.email, 
					"username": request.user.username,
				}
			)

	context['account_form'] = form

	return render(request, "account/account.html", context)







