from django.shortcuts import render
from api.models import Program, UserToken

# Create your views here.


def main(request):

    return render(
        request, 'main.html', {
            "programs": list(Program.objects.filter(owner=request.user)),
            "tokens": list(UserToken.objects.filter(owner=request.user)),
            "user": request.user
        })
