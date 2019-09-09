

from .models import Program, Record, UserToken
from .util import json_response
from django.core.exceptions import ObjectDoesNotExist
import secrets


def serialize_objects(queryset, fields):

    return [
        {k: getattr(obj, k) for k in fields}
        for obj in queryset
    ]


@json_response
def get_records(request, program):

    # Check authentication
    try:
        program = Program.objects.get(pk=program)
    except ObjectDoesNotExist:
        return {"error": "program does not exist"}, 404
    if not secrets.compare_digest(
            request.GET.get('token'), program.access_token):
        return {"error": "invalid token"}, 401

    fields = [
        "record_id", "parent", "name", "desc", "node_id", "type", "start",
        "end", "meta"
    ]

    return {
        "records": serialize_objects(
            Record.objects.filter(program_id=program), fields)
    }, 200


@json_response
def list_programs(request):

    # Check token
    try:
        user = UserToken.objects.get(api_token=request.GET.get('token')).owner
    except ObjectDoesNotExist:
        return {"error": "invalid token"}, 401

    fields = ["api_token", "start", "end"]

    return {
        "programs": serialize_objects(
            Program.objects.filter(owner=user), fields)
    }, 200


@json_response
def delete_token(request):

    # Check token
    try:
        token = UserToken.objects.get(api_token=request.GET.get('token'))
    except ObjectDoesNotExist:
        return {"error": "invalid token"}, 401

    # Delete token
    token.delete()

    return {"success": []}, 200


@json_response
def new_token(request):

    # Check user
    if not request.user.is_authenticated:
        return {"error": "action requires authenticated user"}, 405

    UserToken.objects.create(
        owner=request.user,
        api_token=secrets.token_urlsafe(48),
        desc=request.GET.get('desc', 'New Token'))

    return {"success": []}, 200
