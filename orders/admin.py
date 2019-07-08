from django.contrib import admin
from .models import Order,Refund
# Register your models here.

def make_refund_accepted(modeladmin, request, queryset):
    queryset.update(refund_requested=False, refund_granted=True)

make_refund_accepted.short_description = 'Update orders to refund_granted'

class OrderAdmin(admin.ModelAdmin):
    list_display = ['order_id',
                    'status',
                    'being_delivered',
                    'received',
                    'refund_requested',
                    'refund_granted',
                    'billing_profile',
                    'billing_address',
                     'cart', ]
    
    list_display_links = ['billing_profile',
                          'billing_address',
                          'cart', ]

    list_filter = ['status',
                    'being_delivered',
                    'received',
                    'refund_requested',
                    'refund_granted'] 
    search_fields = [
        'billing_profile__email',
        'order_id',
    ]

    actions = [make_refund_accepted]


admin.site.register(Order,OrderAdmin)
admin.site.register(Refund)



