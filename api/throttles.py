from rest_framework.throttling import SimpleRateThrottle

class FriendRequestThrottle(SimpleRateThrottle):
    scope = 'friend_request'

    def get_cache_key(self, request, view):
        if not request.user.is_authenticated:
            return None  # Only authenticated users are throttled
        return self.cache_format % {
            'scope': self.scope,
            'ident': request.user.pk
        }