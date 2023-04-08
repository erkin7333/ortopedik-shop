from django.contrib import admin
from .models import ClickOrders


class TransactionAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "transaction_type", "status",
                    "is_paid", "is_verified", "is_canceled")
    list_display_links = ("id",)
    list_filter = ("user", "status", "transaction_type", "is_paid", "is_verified", "is_canceled")
    search_fields = ["user__first_name", ]
    list_editable = ("is_paid", "transaction_type", "status")


admin.site.register(ClickOrders, TransactionAdmin)
