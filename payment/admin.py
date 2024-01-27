# payment/admin.py
from django.contrib import admin
from .models import Funds, USDT_TRC20, USDT_ERC20, BTC

# Set custom titles and headers
admin.site.site_header = 'PROVEX HOMES ADMINISTRATION'
admin.site.site_title = 'Provex Admin Portal'
admin.site.index_title = 'Welcome to Provex Homes Admin'

@admin.register(USDT_TRC20)
class USDT_TRC20Admin(admin.ModelAdmin):
    list_display = ('coin_name', 'wallet_address', 'network')
    search_fields = ('coin_name', 'wallet_address')

@admin.register(USDT_ERC20)
class USDT_ERC20Admin(admin.ModelAdmin):
    list_display = ('coin_name', 'wallet_address', 'network')
    search_fields = ('coin_name', 'wallet_address')

@admin.register(BTC)
class BTCAdmin(admin.ModelAdmin):
    list_display = ('coin_name', 'wallet_address', 'network')
    search_fields = ('coin_name', 'wallet_address')


@admin.register(Funds)
class FundsAdmin(admin.ModelAdmin):
    list_display = ('user', 'account_type', 'amount', 'confirmed')
    list_filter = ('user', 'account_type', 'confirmed')
    search_fields = ('user__username', 'account_type', 'confirmed')
    ordering = ('user', 'account_type', 'amount')

    fieldsets = (
        ('User and Account Information', {
            'fields': ('user', 'account_type'),
        }),
        ('Amount Information', {
            'fields': ('amount',),
        }),
        ('Confirmation Information', {
            'fields': ('confirmed',),
        }),
    )

    readonly_fields = ('user', 'account_type')  # make user and account_type read-only in the admin

    def has_add_permission(self, request):
        # Disable the ability to add new funds directly from the admin
        return False
