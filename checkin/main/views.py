from django.shortcuts import render
from api.models import Program, UserToken

def main(request):

    context = {"user": request.user, "server": request.get_host()}
    if request.user.is_authenticated:
        context.update({
            "programs": list(Program.objects.filter(owner=request.user)),
            "tokens": list(UserToken.objects.filter(owner=request.user)),
        })

    return render(request, 'main.html', context)
