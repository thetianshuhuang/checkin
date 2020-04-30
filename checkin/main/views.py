from django.shortcuts import render
from api.models import Program, UserToken


def main(request):

    # Authenticated user
    if request.user.is_authenticated:
        programs = list(Program.objects.filter(owner=request.user))

        return render(
            request, 'main.html', {
                "programs": programs,
                "user": request.user.username,
                "tokens": list(UserToken.objects.filter(owner=request.user))
            })

    # Anonymous user
    else:
        pass
