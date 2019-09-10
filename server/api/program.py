"""Program management API"""

import secrets

from django.core.exceptions import ObjectDoesNotExist

from .models import Program, UserToken
from .util import json_response, serialize_objects


@json_response
def create(request):
    """Create new program.

    Parameters
    ----------
    request : Django request
        Should have the GET parameters:
        - 'token': user API token
        - 'name': desired program name

    Returns
    -------
    JsonResponse
        Created program information, with entries:
        api_token : str
            API token for this program (write access)
        access_token : str
            Access token for this program (read access)
        id : int
            Program ID
        Possible status codes:
        - 401: Invalid token
        - 200: Success
    """

    # Check token
    try:
        user = UserToken.objects.get(api_token=request.GET.get('token')).owner
    except ObjectDoesNotExist:
        return {"error": "invalid token"}, 401

    # Create program
    program = Program.objects.create(
        owner=user,
        api_token=secrets.token_urlsafe(48),
        access_token=secrets.token_urlsafe(48),
        name=request.GET.get('name'),
        start=None,
        end=None)

    # Return token
    return {
        "api_token": program.api_token,
        "access_token": program.access_token,
        "id": program.id
    }, 200


@json_response
def delete(request, program):
    """Delete a program.

    Parameters
    ----------
    request : Django request
        Should have the GET parameter 'token', which should be the program API
        token.
    program : int
        Target program ID

    Returns
    -------
    JsonResponse
        Indicates success or error. Possible status codes:
        - 401: Invalid token
        - 404: Invalid program
        - 200: Success
    """

    # Check authentication
    try:
        program = Program.objects.get(pk=program)
    except ObjectDoesNotExist:
        return {"error": "program does not exist"}, 404
    if not secrets.compare_digest(request.GET.get('token'), program.api_token):
        return {"error": "invalid token"}, 401

    # Delete program
    program.delete()

    return {"success": []}, 200


@json_response
def list(request):
    """List programs owned by a user.

    Parameters
    ----------
    request : Django request
        Should have the GET parameter 'token', which should be a valid user
        token (not a program API or access token).

    Returns
    -------
    JsonResponse
        Follows the format:
        {
            "programs": [
                {
                    "api_token": <str>,
                    "access_token": <str>,
                    "start": <int:posix time>,
                    "end": <int:posix time>,
                    "name": <str>
                }
            ]
        }
        Possible status:
        - 401: Invalid token
        - 200: Success
    """

    # Check token
    try:
        user = UserToken.objects.get(api_token=request.GET.get('token')).owner
    except ObjectDoesNotExist:
        return {"error": "invalid token"}, 401

    fields = ["api_token", "access_token", "start", "end", "name"]

    return {
        "programs": serialize_objects(
            Program.objects.filter(owner=user), fields)
    }, 200
