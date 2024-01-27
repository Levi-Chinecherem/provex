from django.contrib import admin
from .models import Property, PropertyStatus, Investment, CloseInvestment

class PropertyAdmin(admin.ModelAdmin):
    list_display = ('title', 'tag', 'purpose', 'address', 'width_in_sqft', 'no_of_bed', 'no_of_bath')
    list_filter = ('tag', 'purpose')

class PropertyStatusAdmin(admin.ModelAdmin):
    list_display = ('status', 'investors_count')
    filter_horizontal = ('property',)

class InvestmentAdmin(admin.ModelAdmin):
    list_display = ('user', 'property', 'amount', 'interest_percentage', 'created_at')
    list_filter = ('user', 'property', 'created_at')

class CloseInvestmentAdmin(admin.ModelAdmin):
    list_display = ('user', 'property', 'wallet_address', 'network')
    search_fields = ('user__username', 'property__title', 'wallet_address', 'network')
    list_filter = ('network',)

admin.site.register(CloseInvestment, CloseInvestmentAdmin)
admin.site.register(Property, PropertyAdmin)
admin.site.register(PropertyStatus, PropertyStatusAdmin)
admin.site.register(Investment, InvestmentAdmin)
