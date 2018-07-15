"""Decorators for inventory app."""

from django.http import HttpResponse

from json import dumps

from .models import Customuser


def authenticate_user(_view):
    """For authenticating user by access token."""
    def _wrapped_view(request, *args, **kwargs):
        try:
            access_token = request.META.get('HTTP_ACCESS_TOKEN')
        except:
            return HttpResponse(
                dumps({'error_message': 'Invalid Access Token'}),
                content_type='application/json', status=400)

        try:
            user = Customuser.query.filter_by(access_token=access_token).one()
            kwargs['user'] = user
        except:
            return HttpResponse(
                dumps({'error_message': 'Unauthorized User'}),
                content_type='application/json', status=403)

        return _view(request, *args, **kwargs)
    return _wrapped_view
