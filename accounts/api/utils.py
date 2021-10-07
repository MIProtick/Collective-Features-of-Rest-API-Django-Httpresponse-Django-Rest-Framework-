import datetime
from django.conf import settings
from django.utils import timezone
from django.forms.models import model_to_dict

REFRESH_DELAY = settings.JWT_AUTH['JWT_REFRESH_EXPIRATION_DELTA']


def user_dict(user):
    return model_to_dict(user, fields=['username','email','first_name','last_name','id','is_active','is_staff','is_superuser','last_login'])

def jwt_response_payload_handler(token, user=None, request=None):
    return {
        'token': token,
        'user': user_dict(user),
        'expiration': timezone.now() +  REFRESH_DELAY + datetime.timedelta(seconds=200),
    }