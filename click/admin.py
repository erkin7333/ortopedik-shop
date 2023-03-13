
from django.contrib import admin
from .models import ClickOrder


@admin.register(ClickOrder)
class ClickOrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'amount', 'is_paid']
    list_display_links = ['id', 'amount']

    save_on_top = True