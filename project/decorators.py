from django.http import HttpResponse
from django.shortcuts import redirect

def unacthenticated_user(view_func):
    def wrapper_func(request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect("news")
        else:
            return view_func(request, *args, **kwargs)
    return wrapper_func

def allowed_user_types(allowed_roles=[]):
	def decorator(view_func):
		def wrapper_func(request, *args, **kwargs):

			user_type = request.user.get_user_type_display()
			if user_type in allowed_roles:
				return view_func(request, *args, **kwargs)
			else:
				return HttpResponse('You are not authorized to view this page')

		return wrapper_func
	return decorator