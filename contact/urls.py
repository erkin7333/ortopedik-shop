from django.urls import path
from .views import *


app_name = "contact"

urlpatterns = [
    path('contact/', contact, name='contact'),

    path('blog/', blogpage, name='blog')
]