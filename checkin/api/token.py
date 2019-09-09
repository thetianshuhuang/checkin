"""Token management API"""

import secrets

from django.core.exceptions import ObjectDoesNotExist

from .models import UserToken
from .util import json_response


@json_response
def delete(request):
    """Delete a token (revoke all access using that user token)

    Parameters
    ----------
    request : Django request
        Should have the GET parameter 'token', which is the user API token to
        revoke.

    Returns
    -------
    JsonResponse
        Indicates success or failure. Possible status codes:
        - 401: Invalid token
        - 200: Success
    """

    # Check token
    try:
        token = UserToken.objects.get(api_token=request.GET.get('token'))
    except ObjectDoesNotExist:
        return {"error": "invalid token"}, 401

    # Delete token
    token.delete()

    return {"success": []}, 200


@json_response
def new(request):
    """Create new token.

    Parameters
    ----------
    request : Django request
        Must have authenticated user (no API access)

    Returns
    -------
    JsonResponse
        Indicates success or failure. Possible status codes:
        - 405: User not authenticated / API access not allowed
        - 200: Success
    """

    # Check user
    if not request.user.is_authenticated:
        return {"error": "action requires authenticated user"}, 405

    UserToken.objects.create(
        owner=request.user,
        api_token=secrets.token_urlsafe(48),
        desc=request.GET.get('desc', 'New Token'))

    return {"success": []}, 200
