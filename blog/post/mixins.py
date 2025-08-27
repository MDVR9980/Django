from django.shortcuts import redirect

class CustomLoginrequiredMixins:
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect("account:login")
        return super(CustomLoginrequiredMixins, self).dispatch(request, *args, **kwargs)