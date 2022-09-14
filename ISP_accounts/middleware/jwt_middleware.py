from django.contrib.auth.middleware import AuthenticationMiddleware
# from django.utils.functional import SimpleLazyObject
from django.contrib.auth.models import AnonymousUser, User
# from rest_framework_simplejwt.tokens import AccessToken,TokenError,RefreshToken
# from django.conf import settings
from django.http.request import QueryDict
# from django.http.response import HttpResponseRedirect
# from django.urls import reverse_lazy
# from urllib.parse import urlparse, urlunparse
# from django.contrib.auth import views as auth_views
# from django.contrib import messages
# from django.http import HttpResponseForbidden
# from login import *
# from re import compile

''' JWTAuthenticationMiddleware '''
class JWTAuthenticationMiddleware(AuthenticationMiddleware):
    def get_user(self, request):
        user = User()       
           
            