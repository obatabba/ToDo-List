from django.utils.timezone import activate, get_current_timezone
import zoneinfo



class TimezoneMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        user_timezone = request.COOKIES.get('timezone')
        if user_timezone in zoneinfo.available_timezones():
            activate(zoneinfo.ZoneInfo(user_timezone))
        return self.get_response(request)
