from django.utils import timezone
from datetime import timedelta
from rest_framework_simplejwt.authentication import JWTAuthentication

from .models import UserActivity

ACTIVITY_TIMEOUT = timedelta(minutes=5)


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
                now = timezone.now()
                if activity.last_seen and activity.last_seen < now - ACTIVITY_TIMEOUT:
                    logout_at = activity.last_seen + ACTIVITY_TIMEOUT
                    activity.logout_time = logout_at
                    activity.last_seen = logout_at
                    activity.save(update_fields=['logout_time', 'last_seen'])
                    return

                activity.last_seen = now
                activity.save(update_fields=['last_seen'])
        except Exception:
            return
