import datetime
from django.core.cache import cache
from django.conf import settings
from django.utils.deprecation import MiddlewareMixin


class OnlineUserMiddleware(MiddlewareMixin):

    def process_request(self, request):
        user = request.user
        if request.user.is_authenticated:
            now = datetime.datetime.now()
            cache.set(user.username,
                      now,
                      settings.USER_LASTSEEN_TIMEOUT)
