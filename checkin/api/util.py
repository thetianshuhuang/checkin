from django.http import JsonResponse


def json_response(f):
    """Wrapper to create JsonResponse.

    If the function returns a tuple, the first value should be the json data,
    and the second value should be a status code.
    """

    def wrapper(*args, **kwargs):
        out = f(*args, **kwargs)
        if type(out) == tuple:
            return JsonResponse(out[0], status=out[1])
        else:
            return JsonResponse(out)

    return wrapper


def serialize_objects(queryset, fields):

    return [
        {k: getattr(obj, k) for k in fields}
        for obj in queryset
    ]
