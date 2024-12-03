# main/decorators.py
from django.http import HttpResponseForbidden

def adopter_required(view_func):
    def _wrapped_view(request, *args, **kwargs):
        if request.user.account_type != 'user':  # Replace with the actual value of adopter in your model
            return HttpResponseForbidden("You are not authorized to access this page.")
        return view_func(request, *args, **kwargs)
    return _wrapped_view

def shelter_required(view_func):
    def _wrapped_view(request, *args, **kwargs):
        if request.user.account_type != 'shelter':  # Replace with the actual value of shelter in your model
            return HttpResponseForbidden("You are not authorized to access this page.")
        return view_func(request, *args, **kwargs)
    return _wrapped_view
