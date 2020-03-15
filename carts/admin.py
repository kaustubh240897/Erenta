from django.contrib import admin
from .models import Cart,CartItem,Coupon,Quantity

# Register your models here.
def make_refund_accepted(modeladmin, request, queryset):
    queryset.update(refund_requested=False, refund_granted=True)

make_refund_accepted.short_description = 'Update orders to refund_granted'
class CartItemAdmin(admin.ModelAdmin):
    
    list_display = [     'cart',
                         'product',
                        'refund_requested',
                        'refund_granted',
                         'updated' ]
    list_filter = [
                    'refund_requested',
                    'refund_granted']
    list_display_links = ['product' ]
    search_fields = [
        'cart',
        'product',
    ]
    actions = [make_refund_accepted]


admin.site.register(Cart)
admin.site.register(CartItem,CartItemAdmin)
admin.site.register(Coupon)
admin.site.register(Quantity)
