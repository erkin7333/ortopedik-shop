from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls.i18n import i18n_patterns

urlpatterns = i18n_patterns(
    path('makonadminmirzo/', admin.site.urls),
    path('i18n/', include('django.conf.urls.i18n')),
    path('', include('main.urls')),
    path('account', include('account.urls')),
    path('contact', include('contact.urls')),
    path('payment/', include('payment.urls')),
    path('click/', include('click.urls')),

    # path('django_crontab/', include('crontab.urls'))

) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if 'rosetta' in settings.INSTALLED_APPS:
    urlpatterns += [
        path('rosetta/', include('rosetta.urls'))
    ]
