from django.views import View
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from charity_donation_app.models import Donation, Institution, Category
from django.contrib.auth.models import User


# cache for multiple login/register operations
credential_data = {
    'name':         None,
    'surname':      None,
    'email':        None,
    'password':     None,
    'password2':    None
}


class LandingView(View):

    def get(self, request):
        
        def count_packages():
            count = 0

            for donation in Donation.objects.values('quantity'):
                count += donation.get('quantity')
            
            return count


        def count_donated_institutions():
            return len(Donation.objects.values('institution_id').distinct())


        all_instit_foun = Institution.objects.filter(type='foundation')
        all_instit_nongov = Institution.objects.filter(type='non-gov organization')
        all_instit_locfun = Institution.objects.filter(type='local fundraising')


        return render(
            request,
            'index.html',
            context={
                'package_count': count_packages(),
                'institutions': count_donated_institutions(),
                'all_instit_foun': all_instit_foun,
                'all_instit_nongov': all_instit_nongov,
                'all_instit_locfun': all_instit_locfun
            }
        )


class AddDonationView(View):

    def get(self, request):

        if request.user.is_authenticated:
            all_categories = Category.objects.all()

            return render(
                request,
                'form.html',
                context={
                    'all_categories':   all_categories
                }
            )
        
        else:
            return redirect('/login/')


class LoginView(View):

    def get(self, request):
        return render(
            request,
            'login.html'
        )
    
    def post(self, request):

        credential_data['email'] =      request.POST.get('email')
        credential_data['password'] =   request.POST.get('password')

        user = authenticate(
            username=   credential_data['email'],
            password=   credential_data['password']
        )

        if user:
            login(
                request,
                user
            )

            return redirect('/')
        
        else:
            return redirect('/register/')


class RegisterView(View):

    def get(self, request):
        return render(
            request,
            'register.html'
        )

    def post(self, request):

        credential_data['name'] =       request.POST.get('name')
        credential_data['surname'] =    request.POST.get('surname')
        credential_data['email'] =      request.POST.get('email')
        credential_data['password'] =   request.POST.get('password')
        credential_data['password2'] =  request.POST.get('password2')


        # validation placeholder
        def validate_data(self):
            pass


        User.objects.create_user(
            username=       credential_data['email'],
            first_name=     credential_data['name'],
            last_name=      credential_data['surname'],
            email=          credential_data['email'],
            password=       credential_data['password']
        )

        return redirect('/login/')


class LogoutView(View):

    def get(self, request):
        logout(request)

        return redirect('/')