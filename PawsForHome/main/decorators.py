
from django.shortcuts import render

def adopter_required(view_func):
    def _wrapped_view(request, *args, **kwargs):
        if request.user.account_type != 'user':  
            return render(request, '403.html', {}, status=403)
        return view_func(request, *args, **kwargs)
    return _wrapped_view

def shelter_required(view_func):
    def _wrapped_view(request, *args, **kwargs):
        if request.user.account_type != 'shelter': 
            return render(request, '403.html', {}, status=403)
        return view_func(request, *args, **kwargs)
    return _wrapped_view
