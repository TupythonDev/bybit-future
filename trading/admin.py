from django.contrib import admin
from .models import TradingUser

# Register your models here.
class TradingUserAdmin(admin.ModelAdmin):
    list_display = ("user", "is_active", "created_at", "updated_at")
    search_fields = ("user__username", )
    list_filter = ("is_active", "created_at", "updated_at")

    readonly_fields = ("created_at", "updated_at")

    fieldsets = (
        ("Dados do Usuário", {"fields": ("user", "is_active")}),
        ("Informações", {"fields": ("api_key", "api_secret", "testnet")}),
        ("Outros", {"fields": ("created_at", "updated_at")})
    )

admin.site.register(TradingUser, TradingUserAdmin)
