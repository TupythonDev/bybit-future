from django.contrib import admin
from .models import TradingUser, Leverage

# Register your models here.
class TradingUserAdmin(admin.ModelAdmin):
    list_display = ("user", "is_active", "demo", "created_at", "updated_at")
    search_fields = ("user__username", )
    list_filter = ("is_active", "created_at", "updated_at")

    readonly_fields = ("created_at", "updated_at")

    fieldsets = (
        ("Dados do Usuário", {"fields": ("user", "is_active")}),
        ("Informações", {"fields": ("api_key", "api_secret", "demo")}),
        ("Outros", {"fields": ("created_at", "updated_at")})
    )

class LeverageAdmin(admin.ModelAdmin):
    list_display = ('user', 'symbol', 'leverage', 'updated_at')
    list_filter = ('symbol', 'updated_at')
    search_fields = ('user__username', 'symbol')

    readonly_fields = ("updated_at",)

admin.site.register(TradingUser, TradingUserAdmin)
admin.site.register(Leverage, LeverageAdmin)
