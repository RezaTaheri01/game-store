from django.http import HttpRequest


def get_client_ip(request: HttpRequest):
    x_forward_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forward_for:
        ip = x_forward_for.split(',')
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip
