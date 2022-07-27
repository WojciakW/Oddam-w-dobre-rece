from django.shortcuts import render
from django.views import View
from django.shortcuts import render

# Create your views here.

class LandingView(View):
    def get(self, request):
        return render(
            request,
            'index.html'
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