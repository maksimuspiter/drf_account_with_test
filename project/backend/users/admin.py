from django.contrib import admin
from .models import Account
from rest_framework.authtoken.admin import TokenAdmin

TokenAdmin.raw_id_fields = ["user"]


@admin.register(Account)
class AccountAdmin(admin.ModelAdmin):
    pass
