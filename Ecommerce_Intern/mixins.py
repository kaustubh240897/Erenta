from django.utils.http import is_safe_url

class RequestFormAttachMixin(object):
    def get_form_kwargs(self):
        kwargs = super(RequestFormAttachMixin, self).get_form_kwargs()
        kwargs['request'] = self.request
        return kwargs

class NextUrlMixin(object):
    default_next = "/"
    def get_next_url(self):
        request = self.request
        city = request.session.get('city_names',None)
        if city == "Tokyo":
            self.default_next = "/home/Tokyo"
        elif city == "Osaka":
            self.default_next = "/home/Osaka"
        elif city == "Kyoto":
            self.default_next = "/home/Kyoto"
        else:
            self.default_next = "/home/Tokyo"
        next_ = request.GET.get('next')
        next_post = request.POST.get('next')
        redirect_path = next_ or next_post or None
        if is_safe_url(redirect_path, request.get_host()):
            return redirect_path
        return self.default_next
