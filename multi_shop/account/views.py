from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views import View
from .forms import LoginForm, RegisterForm, CheckOtpForm
# import ghasedakpack
from random import randint
# from django.utils.crypto import get_random_string
from .models import User, Otp
from uuid import uuid4

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
            cd = form.cleaned_data
            user = authenticate(username=cd['phone'], password=cd['password'])
            if user is not None:
                login(request, user)
                return redirect("/")
            else:
                form.add_error("phone", "invalid user data")
        else:
            form.add_error("phone", "invalid data")
        return render(request, "account/login.html", {'form': form})
    
class OtpLoginView(View):
    def get(self, request):
        form = RegisterForm
        return render(request, "account/otp_login.html", {'form': form})

    def post(self, request):
        form = RegisterForm(request.POST)
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
            Otp.objects.create(phone=cd['phone'], code=randcode, token=token)
            print(randcode)
            return redirect(reverse('account:check_otp') + f'?token={token}')

        else:
            form.add_error("phone", "invalid data")
        return render(request, "account/otp_login.html", {'form': form})
    

class CheckOtpView(View):
    def get(self, request):
        form = CheckOtpForm()
        return render(request, "account/check_otp.html", {'form': form})

    def post(self, request):
        token = request.GET.get('token')
        form = CheckOtpForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            if Otp.objects.filter(code=cd['code'], token=token).exists():
                otp = Otp.objects.get(token=token)
                # user = User.objects.create_user(phone=otp.phone)
                user, is_created = User.objects.get_or_create(phone=otp.phone)
                # IMPORTANT: set the backend before login when multiple backends exist
                user.backend = 'django.contrib.auth.backends.ModelBackend'
                login(request, user)
                otp.delete()
                return redirect("/")
        else:
            form.add_error("phone", "invalid data")
        return render(request, "account/check_otp.html", {'form': form})