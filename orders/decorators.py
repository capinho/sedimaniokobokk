from django.contrib.auth import REDIRECT_FIELD_NAME
from django.contrib.auth.decorators import user_passes_test
from datetime import timedelta
import datetime
from django.core.exceptions import PermissionDenied
from .models import *


def cart(function):
    def wrap(request, *args, **kwargs):
            cart = Cart(request)
            for item in cart:

            if cart!=0:
                raise PermissionDenied
            else:
                return function(request, *args, **kwargs)
    wrap.__doc__=function.__doc__
    wrap.__name__=function.__name__
    return wrap
