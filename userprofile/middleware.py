from django.utils import timezone
from django.core.cache import cache
from django.conf import settings
from django.utils.deprecation import MiddlewareMixin
from rest_framework.authtoken.models import Token
from re import sub


class OnlineUserMiddleware(MiddlewareMixin):

    def process_request(self, request):
        header_token = request.META.get('HTTP_AUTHORIZATION', None)
        if header_token is not None:
            try:
                token = sub('Token ', '', request.META.
                            get('HTTP_AUTHORIZATION', None))
                token_obj = Token.objects.get(key=token)
                request.user = token_obj.user
            except Token.DoesNotExist:
                pass
        user = request.user
        if request.user.is_authenticated:
            now = timezone.now()
            cache.set(user.username,
                      now,
                      settings.USER_LASTSEEN_TIMEOUT)
