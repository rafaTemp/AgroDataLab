from django.http import HttpResponse
from django.contrib.auth.decorators import login_required

@login_required
def inicio(request):
    return HttpResponse("Bienvenido a EnviroProRecord")
