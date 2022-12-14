"""charity_donation URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from charity_donation_app import views

urlpatterns = [
    path(
        'admin/', 
        admin.site.urls
    ),
    path(
        '',
        views.LandingView.as_view()
    ),
    path(
        'login/',
        views.LoginView.as_view()
    ),
    path(
        'register/',
        views.RegisterView.as_view()
    ),
    path(
        'add_donation/',
        views.AddDonationView.as_view()
    ),
    path(
        'donation_confirm/',
        views.DonationConfirmView.as_view()
    ),
    path(
        'logout/',
        views.LogoutView.as_view()
    ),
    path(
        'profile/',
        views.ProfileView.as_view()
    ),
    path(
        'settings/',
        views.SettingsView.as_view()
    ),
    path(
        'change_password/',
        views.ChangePasswordView.as_view()
    ),
    path(
        'change_data/',
        views.ChangeUserDataView.as_view()
    )
]
