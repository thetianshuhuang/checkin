from django.http import JsonResponse


def json_response(f):

    def wrapper(*args, **kwargs):
        return JsonResponse(f(*args, **kwargs))

    return wrapper
