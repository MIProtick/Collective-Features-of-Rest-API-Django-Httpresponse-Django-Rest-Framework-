from django.http import HttpResponse


def custom_response(data, is_json=True, status=200):
    if is_json:
        content_type = 'application/json'
    else:
        content_type = 'text/html'

    return HttpResponse(data, content_type=content_type, status=status)
