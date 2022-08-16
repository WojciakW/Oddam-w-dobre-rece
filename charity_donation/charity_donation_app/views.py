from django.views import View
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from charity_donation_app.models import Donation, Institution, Category
from django.contrib.auth.models import User
from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404


class CredentialValidator:

    credential_data = {
        'name':         '',
        'surname':      '',
        'email':        '',
        'password':     '',
        'password2':    ''
    }
        

    @staticmethod
    def validate_username():

        try: 
            User.objects.get(username=CredentialValidator.credential_data['email'])
            return False
        
        except User.DoesNotExist:
            return True

    @staticmethod
    def validate_password():

        tests = {
            'same_password': False,
            'long_password': False,
            'not_null_password': False
        }
        
        if CredentialValidator.credential_data['password'] == CredentialValidator.credential_data['password2']:
            tests['same_password'] = True

        if len(CredentialValidator.credential_data['password']) >= 8:
            tests['long_password'] = True

        if CredentialValidator.credential_data['password'] != '':
            tests['not_null_password'] = True

        if False in tests.values():
            return (
                tests,
                False
            )
        
        return (
            None,
            True
        )

    @staticmethod
    def validate_email():

        if '@' not in CredentialValidator.credential_data['email']:
            return False
        
        return True
    
    @staticmethod
    def validation_output(*args, **kwargs):

        msg = []

        if 'username' in args:
            is_valid_username = CredentialValidator.validate_username()

            if not is_valid_username:
                msg.append("Użytkownik o podanym adresie email już istnieje")
        
        if 'password' in args:
            password_validation = CredentialValidator.validate_password()
            is_valid_password = password_validation[1]

            if not is_valid_password:
                if not password_validation[0].get('same_password'):
                    msg.append("Podane hasła nie są takie same")
                
                if not password_validation[0].get('long_password'):
                    msg.append("Podane hasło jest za krótkie (co najmniej 8 znaków)")
                
                if not password_validation[0].get('not_null_password'):
                    msg.append("Hasło nie może być puste")
        
        if 'email' in args:
            is_valid_email = CredentialValidator.validate_email()
        
            if not is_valid_email:
                msg.append("Niepoprawna forma adresu email")

        return msg


class LandingView(View):

    def get(self, request):
        
        def count_packages():
            count = 0

            for donation in Donation.objects.values('quantity'):
                count += donation.get('quantity')
            
            return count

        def count_donated_institutions():
            return len(Donation.objects.values('institution_id').distinct())

        all_instit_foun =   Institution.objects.filter(type='foundation')
        all_instit_nongov = Institution.objects.filter(type='non-gov organization')
        all_instit_locfun = Institution.objects.filter(type='local fundraising')

        return render(
            request,
            'index.html',
            context={
                'package_count':        count_packages(),
                'institutions':         count_donated_institutions(),
                'all_instit_foun':      all_instit_foun,
                'all_instit_nongov':    all_instit_nongov,
                'all_instit_locfun':    all_instit_locfun
            }
        )


class AddDonationView(View):

    def get(self, request):

        if request.user.is_authenticated:
            all_categories = Category.objects.all()
            all_institutions = Institution.objects.all()

            return render(
                request,
                'form.html',
                context={
                    'all_categories':   all_categories,
                    'all_institutions': all_institutions
                }
            )
        
        else:
            return redirect('/login/')

    def post(self, request):

        new_donation = Donation(
            quantity=           request.POST.get('bags'),
            institution_id=     request.POST.get('institution'),
            address=            request.POST.get('address'),
            phone_number=       request.POST.get('phone'),
            city=               request.POST.get('city'),
            zip_code=           request.POST.get('postcode'),
            pick_up_date=       request.POST.get('data'),
            pick_up_time=       request.POST.get('time'),
            pick_up_comment=    request.POST.get('more_info'),
            user_id=            request.user.id
        )

        categories_list = request.POST.getlist('categories')

        new_donation.save()

        for category in categories_list:
            new_donation.categories.add(category)

        new_donation.save()

        return redirect('/donation_confirm/')


class DonationConfirmView(View):

    def get(self, request):
        return render(
            request,
            'form-confirmation.html'
        )


class LoginView(View):

    def get(self, request):
        return render(
            request,
            'login.html'
        )
    
    def post(self, request):

        CredentialValidator.credential_data['email'] =      request.POST.get('email')
        CredentialValidator.credential_data['password'] =   request.POST.get('password')

        user = authenticate(
            username=   CredentialValidator.credential_data['email'],
            password=   CredentialValidator.credential_data['password']
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

        CredentialValidator.credential_data['name'] =       request.POST.get('name')
        CredentialValidator.credential_data['surname'] =    request.POST.get('surname')
        CredentialValidator.credential_data['email'] =      request.POST.get('email')
        CredentialValidator.credential_data['password'] =   request.POST.get('password')
        CredentialValidator.credential_data['password2'] =  request.POST.get('password2')

        msg = CredentialValidator.validation_output(
            'password',
            'email',
            'username'
        )

        if msg == []:
            User.objects.create_user(
                username=       CredentialValidator.credential_data['email'],
                first_name=     CredentialValidator.credential_data['name'],
                last_name=      CredentialValidator.credential_data['surname'],
                email=          CredentialValidator.credential_data['email'],
                password=       CredentialValidator.credential_data['password']
            )

            return redirect('/login/')

        else:
            return render(
            request,
            'register.html',
            context={
                'msg': msg
            }
        )
 

class LogoutView(View):

    def get(self, request):
        logout(request)

        return redirect('/')


class ProfileView(View):

    def get(self, request):

        if request.user.is_authenticated:

            user = request.user
            user_donations = Donation.objects.filter(user_id=user.id).order_by('is_taken')

            return render(
                request,
                'user_profile.html',
                context={
                    'user': user,
                    'user_donations': user_donations
                }
            )

        else:
            raise PermissionDenied()
    
    def post(self, request):

        if request.user.is_authenticated:
            
            donation_id = request.POST.get('donation')
            donation = get_object_or_404(Donation, id=donation_id)

            donation.is_taken = True
            donation.save()

            return redirect('/profile/')

        else:
            raise PermissionDenied()


class SettingsView(View):

    def get(self, request):

        if request.user.is_authenticated:
            
            return render(
                request,
                'user_settings.html'
            )

        else:
            raise PermissionDenied()


class ChangePasswordView(View):

    def get(self, request):

        if request.user.is_authenticated:

            return render(
                request,
                'user_change_password.html'
            )
        
        else:
            raise PermissionDenied()
    
    def post(self, request):

        user_authenticate = authenticate(
            username=request.user.username,
            password=request.POST.get('old_password')
        )

        if not user_authenticate:
            msg = ["Nieprawidłowe obecne hasło"]

            return render(
                request,
                'user_change_password.html',
                context={
                    'msg': msg
                }
            )
        
        else:     
            CredentialValidator.credential_data['password']     = request.POST.get('new_password')
            CredentialValidator.credential_data['password2']    = request.POST.get('new_password2')

            msg = CredentialValidator.validation_output('password')

            if msg == []:
                user = User.objects.get(id=request.user.id)
                user.set_password(CredentialValidator.credential_data['password'])
                user.save()

                authenticate(
                    username=user.username,
                    password=user.password
                )

                login(
                    request,
                    user
                )

                return redirect('/settings/')
            
            else:
                return render(
                    request,
                    'user_change_password.html',
                    context={
                        'msg': msg
                    }
                )


class ChangeUserDataView(View):

    def get(self, request):

        if request.user.is_authenticated:

            return render (
                request,
                'user_change_data.html',
                context ={
                    'user': request.user
                }
            )
        
        else:
            raise PermissionDenied()

    def post(self, request):

        user_authenticate = authenticate(
            username=request.user.username,
            password=request.POST.get('password')
        )

        if not user_authenticate:
            msg = ["Nieprawidłowe hasło"]

            return render(
                request,
                'user_change_data.html',
                context={
                    'msg': msg
                }
            )
        
        else:
            user = request.user

            user.first_name = request.POST.get('first_name')
            user.last_name = request.POST.get('last_name')
            user.save()

            return redirect('/settings/')