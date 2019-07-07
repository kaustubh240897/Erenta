from django.shortcuts import render
from django.views.generic import CreateView
from .models import OtherDetails
from products.models import Product_description
from carts.forms import OtherDetailForm
from django.shortcuts import  get_object_or_404
# Create your views here.


class OtherDetailsView(CreateView):
    
    model = OtherDetails
    form_class = OtherDetailForm
    template_name = 'products/detail.html'
    
    
    
    def form_valid(self, form):
        article = form.save(commit=False)
        article.user = self.request.user
         
        #article.save()  # This is redundant, see comments.
        return super(OtherDetailsView, self).form_valid(form) 
    

    def get_success_url(self):
        return reverse("other")
    

# def other_details_view(request):
#    otherdetail_form = OtherDetailForm(request.POST or None)
#    #product = get_object_or_404(Product_description, slug=slug)
#    context = {
#        "title":"details",
#        "content":"Add your details",
#         "form": otherdetail_form,

#     }

    
   
#    if request.method== "POST":
#        quantity =request.POST.get('quantity')
#        size=request.POST.get('size')
#        days=request.POST.get('days')
#        other_details=request.POST.get('other_details')
#        contact = OtherDetails(quantity=quantity, size=size, days=days, other_details=other_details)
#        contact.save()
       
#    if otherdetail_form.is_valid():
#        print(OtherDetailForm.cleaned_data)
       
      
   

   

#    return render(request,"contact/contactform.html",context)




