from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views import View
from .forms import LoginForm, OtpLoginForm, CheckOtpForm
# import ghasedakpack
from random import randint
# from django.utils.crypto import get_random_string
from .models import User, Otp
from uuid import uuid4
from datetime import timedelta
from django.utils import timezone

# def user_login(request):
#     return render(request, "account/login.html", {})

# SMS = ghasedakpack.Ghasedak('') # add api key

class UserLogin(View):
    def get(self, request):
        form = LoginForm()
        return render(request, "account/login.html", {'form': form})

    def post(self, request):
        form = LoginForm(request.POST)
        if form.is_valid():
            identifier = form.cleaned_data['identifier']
            password = form.cleaned_data['password']

            # Authenticate using the unified identifier
            user = authenticate(request, username=identifier, password=password)

            if user is not None:
                login(request, user)
                return redirect("/")
            else:
                # Do not reveal too much; generic error
                form.add_error(None, "Invalid username or password.")
        # If form is invalid, it will render with errors
        return render(request, "account/login.html", {'form': form})
    
class OtpLoginView(View):
    def get(self, request):
        form = OtpLoginForm()
        return render(request, "account/otp_login.html", {'form': form})

    def post(self, request):
        form = OtpLoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            randcode = randint(1000, 9999)
            # SMS.verification(
            #     {
            #         'receptor': cd["phone"], # number phone reciver
            #         'type': '1',
            #         'template': 'randcode',
            #         'code': randcode,
            #     }
            # )
            # token = get_random_string(length=100)
            token = str(uuid4())
            Otp.objects.create(
                phone=cd['phone'],
                code=randcode, 
                token=token,
                expiration_date=timezone.now() + timedelta(minutes=1) # expire time is 1 min   
            )
            print(randcode)
            return redirect(reverse('account:check_otp') + f'?token={token}')

        else:
            form.add_error("phone", "invalid data")
        return render(request, "account/otp_login.html", {'form': form})
    

# class CheckOtpView(View):
#     def get(self, request):
#         form = CheckOtpForm()
#         return render(request, "account/check_otp.html", {'form': form})

#     def post(self, request):
#         token = request.GET.get('token')
#         form = CheckOtpForm(request.POST)
#         if form.is_valid():
#             cd = form.cleaned_data
#             if Otp.objects.filter(code=cd['code'], token=token).exists():
#                 otp = Otp.objects.get(token=token)
#                 # user = User.objects.create_user(phone=otp.phone)
#                 user, is_created = User.objects.get_or_create(phone=otp.phone)
#                 # IMPORTANT: set the backend before login when multiple backends exist
#                 user.backend = 'django.contrib.auth.backends.ModelBackend' # or login(request, user, backend='django.contrib.auth.backends.ModelBackend')
#                 login(request, user)
#                 otp.delete()
#                 return redirect("/")
#         else:
#             form.add_error("phone", "invalid data")
#         return render(request, "account/check_otp.html", {'form': form})



class CheckOtpView(View):
    def get(self, request):
        """
        Display the OTP verification form.
        """
        form = CheckOtpForm()
        return render(request, "account/check_otp.html", {'form': form})

    def post(self, request):
        """
        Validate the OTP for the provided token and log in the user if valid.
        Also handles expired OTPs.
        """
        token = request.GET.get('token')
        form = CheckOtpForm(request.POST)

        if form.is_valid():
            cd = form.cleaned_data

            # 1) Retrieve the OTP associated with the token and code
            try:
                otp = Otp.objects.get(token=token, code=cd['code'])
            except Otp.DoesNotExist:
                form.add_error("code", "Invalid OTP.")
                return render(request, "account/check_otp.html", {'form': form})

            # 2) Check expiration
            if otp.expiration_date and otp.expiration_date < timezone.now():
                otp.delete()
                form.add_error("code", "OTP has expired. Please request a new one.")
                return render(request, "account/check_otp.html", {'form': form})

            # 3) Authenticate / Create user and login
            otp_phone = otp.phone
            user, is_created = User.objects.get_or_create(phone=otp_phone)

            # IMPORTANT: set the backend before login when multiple backends exist
            user.backend = 'django.contrib.auth.backends.ModelBackend'
            login(request, user)

            # 4) Clean up OTP
            otp.delete()

            return redirect("/")

        else:
            # If form is invalid, attach an error to the phone field for consistency
            form.add_error("phone", "invalid data")

        return render(request, "account/check_otp.html", {'form': form})
    
def user_logout(request):
    logout(request)
    return redirect("/")