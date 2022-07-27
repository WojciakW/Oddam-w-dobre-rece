from itertools import count
from django.views import View
from django.shortcuts import render
from charity_donation_app.models import Donation, Institution
from django.contrib.auth.models import User


class LandingView(View):

    def get(self, request):
        
        def count_packages():
            count = 0

            for donation in Donation.objects.values('quantity'):
                count += donation.get('quantity')
            
            return count


        def count_donated_institutions():
            return len(Donation.objects.values('institution_id').distinct())


        return render(
            request,
            'index.html',
            context={
                'package_count': count_packages(),
                'institutions': count_donated_institutions()
            }
        )


class AddDonationView(View):

    def get(self, request):
        return render(
            request,
            'form.html'
        )


class LoginView(View):

    def get(self, request):
        return render(
            request,
            'login.html'
        )


class RegisterView(View):

    def get(self, request):
        return render(
            request,
            'register.html'
        )