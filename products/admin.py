from django.contrib import admin
from .models import Product_description,Contact,User_Review,Supplier_Review
# Register your models here.
class ProductAdmin(admin.ModelAdmin):
    list_display= ['__str__', 'slug']
    class Meta:
        model=Product_description
    def get_changeform_initial_data(self, request):
        get_data = super(ProductAdmin, self).get_changeform_initial_data(request)
        get_data['user'] = request.user.pk
        return get_data


admin.site.register(Product_description, ProductAdmin)
admin.site.register(Contact)
admin.site.register(User_Review)
admin.site.register(Supplier_Review)


