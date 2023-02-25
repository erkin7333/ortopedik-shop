from django.contrib import admin
from .models import Blog, Contact, Requestforhelp
from parler.admin import TranslatableAdmin
# Register your models here.



class ContactAdmin(TranslatableAdmin):
    list_display = ('id', 'name', 'subject',
                    'address', 'phone', 'email')
    list_display_links = ('name',)

admin.site.register(Contact, ContactAdmin)


class RequestforhelpAdmin(admin.ModelAdmin):
    list_display = ('id', 'full_name', 'email', 'phone', 'company', 'description')
    list_display_links = ('full_name', 'phone')

admin.site.register(Requestforhelp, RequestforhelpAdmin)


class BlogAdmin(TranslatableAdmin):
    list_display = ('id', 'subject', 'description', 'image')
    list_display_links = ('subject',)
    list_per_page = 5
    search_fields = ('subject',)

admin.site.register(Blog, BlogAdmin)