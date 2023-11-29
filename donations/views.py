from django.contrib import messages
from django.core.mail import send_mail
from django.http import HttpResponse
from django.shortcuts import render, redirect
from .forms import DonationForm
from .models import Donation
from django.contrib.auth.decorators import user_passes_test
from django.db.models import Q
from .credentials import *
import requests
from django.conf import settings
import json
from requests.auth import HTTPBasicAuth


# Create your views here.
def is_superuser(user):
    return user.is_superuser


def donations(request):
    if 'q' in request.GET:
        q = request.GET.get('q', '')
        donation = Donation.objects.filter(Q(name__icontains=q) | Q(phone__icontains=q) | Q(purpose__icontains=q))
    else:
        donation = Donation.objects.all()
    context = {"donations": donation}
    return render(request, 'donations/donations.html', context)


@user_passes_test(is_superuser, login_url='error_message-url')
def add_form(request):
    if request.method == "POST":
        form = DonationForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Product saved successfully')
            return redirect("donations-url")
        else:
            messages.error(request, 'Product saving failed')
            return redirect("donations-url")
    else:
        form = DonationForm()
    return render(request, 'donations/add-form.html', {"form": form})


@user_passes_test(is_superuser, login_url='error_message-url')
def update_form(request, id):
    donation = Donation.objects.get(id=id)
    if request.method == "POST":
        recipient_name = request.POST.get('name')
        recipient_phone_no = request.POST.get('phone')
        donation_purpose = request.POST.get('purpose')

        donation.name = recipient_name
        donation.phone = recipient_phone_no
        donation.purpose = donation_purpose
        donation.save()
        messages.success(request, 'Form updated successfully')
        return redirect('donations-url')
    return render(request, 'donations/update.html', {'donation': donation})


@user_passes_test(is_superuser, login_url='error_message-url')
def delete_form(request, id):
    donation = Donation.objects.get(id=id)
    donation.delete()
    messages.success(request, 'Product deleted successfully')
    return redirect('donations-url')


def pay(request, id):
    donation = Donation.objects.get(id=id)
    if request.method == "POST":
        sender_phone_number = request.POST.get('phone', '')
        recipient_phone_number = donation.phone
        amount = request.POST.get('price', '')
        recipient_name = donation.name
        access_token = MpesaAccessToken.validated_mpesa_access_token
        api_url = "https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest"
        headers = {"Authorization": "Bearer %s" % access_token}
        payload = {
            "BusinessShortCode": LipanaMpesaPassword.Business_short_code,
            "Password": LipanaMpesaPassword.decode_password,
            "Timestamp": LipanaMpesaPassword.lipa_time,
            "TransactionType": "CustomerPayBillOnline",
            "Amount": amount,
            "PartyA": sender_phone_number,  # Assuming sender is the customer initiating the payment
            "PartyB": LipanaMpesaPassword.Business_short_code,
            "PhoneNumber": sender_phone_number,  # Recipient's phone number
            "CallBackURL": "https://sandbox.safaricom.co.ke/mpesa/",
            "AccountReference": "PYMENT001",
            "TransactionDesc": f"Pay {amount} to {recipient_name} ({recipient_phone_number})"
        }

        response = requests.post(api_url, json=payload, headers=headers)

        # Handle the response accordingly
        if response.status_code == 200:
            # Payment was successful
            return HttpResponse('Success')
        else:
            # Handle the error
            print(response.text)
            return HttpResponse(f'Failure. Error:{response.text}')

    return render(request, 'donations/donate.html', {'donation': donation})


def contact_view(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        subject = request.POST.get('subject')
        message = request.POST.get('message')

        email_message = f'Name: {name}\nEmail: {email}\nMessage: {message}\nSubject: {subject}'

        from_email = email
        recipient_list = ['donationplatform2003@gmail.com']

        send_mail(subject, email_message, from_email, recipient_list)
        return redirect('success-page-url')  # Create a success page

    return render(request, 'donations/contact.html')


def error_message(request):
    return render(request, 'donations/error_message.html')


def password_reset(request):
    return render(request, 'donations/password_reset.html')


def password_reset_done(request):
    return render(request, 'donations/password_reset_done.html')


def reset_done(request):
    return render(request, 'donations/reset_done.html')


def reset_set_password(request):
    return render(request, 'donations/reset_set_password.html')


def success_page(request):
    return render(request, 'donations/success-page.html')


def about(request):
    return render(request, 'about.html')
