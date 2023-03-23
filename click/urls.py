from django.urls import path
from click.views import *

app_name = "click"

urlpatterns = [
    path('', click_method, name='click_p'),
    path('click/transaction/', OrderTestView.as_view(), name="transaction"),
    path('uzclick/', CreateClickOrderView.as_view(), name='uzclick')
]
