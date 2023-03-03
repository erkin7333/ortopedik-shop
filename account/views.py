from django.shortcuts import render, redirect
from django.views.generic import View
from .forms import RegistrationForm, LoginForm
from django.contrib.auth import authenticate, login, logout
from .models import User
import requests
from config import settings


class UserRegistration(View):
    """Foydalanuvchilarni ro'yxatdan o'tkazish uchun Class based views"""

    def setup(self, request, *args, **kwargs):
        super().setup(request, *args, **kwargs)

    def get(self, request):
        form = RegistrationForm()
        context = {
            'form': form
        }
        return render(request, 'account/register.html', context=context)

    def post(self, request):
        form = RegistrationForm(data=request.POST)
        if form.is_valid():
            data = form.cleaned_data
            del data['confirm']
            user = User(**data)
            user.set_password(data['password'])
            username = data['username']
            phone = data['phone']
            user.save()
            """Foydalanuvchini nomi va telefon raqamini KPI api siga saqlash"""

            api_url = "https://apps.kpi.com/services/api/v3/customer/create"
            payload = {
                    "name": username,
                    "phone": phone
            }
            headers = {
                "Content-Type": "application/json",
                "Accept": "application/json",
                "accessToken": settings.ACCESS_TOKEN,
                "x-auth": settings.X_TOKEN
            }
            print("SSSSSSSSSSSSSSSSSSSs", settings.ACCESS_TOKEN, settings.X_TOKEN)
            response = requests.post(api_url, json=payload, headers=headers)
            if response.status_code == 200:
                response_data = response.json()
                print("DATA=================", response_data)
                data_id = response_data.get('data', {}).get("id")
                print("SUCCESS ID ===========================", data_id)
                user.kpi_id = data_id
                print("ID==================", user.kpi_id)
                user.save()
                return redirect('account:login')

            else:

                context = {
                    'form': form,
                    'error': "Palumot kiritilmadi"
                }
                return render(request, 'account/register.html', context=context)
        context = {
            'form': form
        }
        return render(request, 'account/register.html', context=context)


class UserLogin(View):
    """Tizimga kirish uchun Class based views"""

    def setup(self, request, *args, **kwargs):
        super().setup(request, *args, **kwargs)

    def get(self, request):
        form = LoginForm()
        context = {
            'form': form
        }
        return render(request, 'account/login.html', context=context)

    def post(self, request):
        form = LoginForm(data=request.POST)
        if form.is_valid():
            user = authenticate(username=form.cleaned_data['username'], password=form.cleaned_data['password'])
            if user is not None:
                login(request, user)
                return redirect('main:home')
            form.add_error('password', "Username yoki parol noto'g'ri")

        return render(request, 'account/login.html', {'form': form})


def user_logout(request):
    """User Logout"""
    logout(request)
    return redirect('main:home')
