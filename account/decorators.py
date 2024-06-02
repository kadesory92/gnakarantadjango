from functools import wraps

from django.core.exceptions import PermissionDenied
from django.shortcuts import redirect


def required_role(role):
    def decorator(view_func):
        @wraps(view_func)
        def wrapped_view(request, *args, **kwargs):
            if request.user.is_authenticated and request.user.role == role:
                return view_func(request, *args, **kwargs)
            else:
                return redirect('login')  # Redirect to login if user doesn't have the required role

        return wrapped_view

    return decorator


def role_required(roles):
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            if not request.user.is_authenticated:
                raise PermissionDenied("You are not logged in.")
            if request.user.role not in roles:
                raise PermissionDenied("You do not have the required role.")
            return view_func(request, *args, **kwargs)

        return _wrapped_view

    return decorator


def has_role(user, roles):
    return user.role in roles


def is_school_role(user):
    return user.role in ['SCHOOL', 'SCHOOL_ADMIN', 'SCHOOL_MANAGER']