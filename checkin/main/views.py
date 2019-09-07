from django.shortcuts import render
from api.models import Program

# Create your views here.


def main(request):

    programs = list(Program.objects.filter(owner=request.user))

    return render(
        request, 'main.html', {"programs": programs, "user": request.user.username})
