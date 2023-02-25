from django.urls import path
from .views import *


app_name = 'account'

urlpatterns = [
    path('', UserRegistration.as_view(), name='register'),

    path('login/', UserLogin.as_view(), name='login'),

    path('logout/', user_logout, name='logout')
]