from django.contrib import admin
from .models import Product_description,Contact,Review
# Register your models here.
class ProductAdmin(admin.ModelAdmin):
    list_display= ['__str__', 'slug']
    class Meta:
        model=Product_description


admin.site.register(Product_description, ProductAdmin)
admin.site.register(Contact)
admin.site.register(Review)


