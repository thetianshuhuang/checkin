from django.http import JsonResponse


def json_response(f):

    def wrapper(*args, **kwargs):
        out = f(*args, **kwargs)
        if type(out) == tuple:
            return JsonResponse(out[0], status=out[1])
        else:
            return JsonResponse(out)

    return wrapper
