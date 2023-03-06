from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django_crontab import crontab

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('main.urls')),
    path('account', include('account.urls')),
    path('contact', include('contact.urls')),
    # path('django_crontab/', include('crontab.urls'))

] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

