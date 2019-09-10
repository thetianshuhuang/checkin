from django.shortcuts import render
from api.models import Program, UserToken

# Create your views here.


def main(request):

    context = {"user": request.user}
    if request.user.is_authenticated:
        context.update({
            "programs": list(Program.objects.filter(owner=request.user)),
            "tokens": list(UserToken.objects.filter(owner=request.user)),
        })

    return render(request, 'main.html', context)
