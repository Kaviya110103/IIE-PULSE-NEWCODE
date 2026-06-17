from django.utils import timezone
from rest_framework_simplejwt.authentication import JWTAuthentication

from .models import UserActivity


class UserActivityLastSeenMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.jwt_authentication = JWTAuthentication()

    def __call__(self, request):
        self._update_last_seen(request)
        return self.get_response(request)

    def _update_last_seen(self, request):
        try:
            if not request.path.startswith('/api/'):
                return

            authenticated = self.jwt_authentication.authenticate(request)
            if not authenticated:
                return

            user, _token = authenticated
            activity = UserActivity.objects.filter(
                user=user,
                logout_time__isnull=True,
            ).order_by('-login_time').first()

            if activity:
                activity.last_seen = timezone.now()
                activity.save(update_fields=['last_seen'])
        except Exception:
            return
